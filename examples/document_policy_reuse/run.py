"""Offline synthetic document-access decision benchmark; no customer data or model calls."""
from collections import Counter
from copy import deepcopy
from datetime import date
import json
import statistics
from time import perf_counter_ns
from jsonschema import Draft202012Validator
from kora.solution.economics import EconomicsNode, ExecutionPolicy, WorkloadEconomicsRunner

ACTIONS = ("allow", "redact", "deny", "refresh")
def schema(key, vals):
    return {"type":"object","properties":{key:{"enum":list(vals)}},"required":[key],"additionalProperties":False}
NODES = (
    EconomicsNode("classify","Classify synthetic document","routine",output_schema=schema("classification",("public","internal","restricted"))),
    EconomicsNode("authorize","Determine permitted read mode","routine",("classify",),output_schema=schema("action",ACTIONS)),
    EconomicsNode("notice","Emit action code without document content","routine",("authorize",),output_schema=schema("notice",ACTIONS)),
)
def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"))

class Fixture:
    def __init__(self):
        self.calls=Counter()
        self.version="v1"
    def cache_identity(self):
        return {"fixture_version":self.version}
    def run(self,*,task_id,input,budget,output_schema):
        self.calls[task_id]+=1
        b=input["workload"]["brief"]
        d=input["dependencies"]
        if task_id=="classify":
            output={"classification":input["workload"]["document"]["classification"]}
        elif task_id=="authorize":
            c=d["classify"]["classification"]
            if not b["granted"]:
                a="deny"
            elif date.fromisoformat(b["as_of"])>date.fromisoformat(b["expires"]):
                a="refresh"
            elif c=="public":
                a="allow"
            elif c=="internal" and b["role"]=="staff":
                a="allow"
            elif c=="internal" and b["redaction_allowed"]:
                a="redact"
            else:
                a="deny"
            output={"action":a}
        elif task_id=="notice":
            output={"notice":d["authorize"]["action"]}
        else:
            raise ValueError(task_id)
        return {"ok":True,"output":output,"meta":{"provider":"deterministic-fixture","model_calls":0},"usage":{}}

# Explicit authored oracle: not computed by the adapter. Each phase changes one
# or more trusted context fields. All documents are fabricated classifications.
BASE={"tenant":"alpha","principal":"u1","role":"guest","granted":True,
      "grant_epoch":1,"policy_epoch":1,"redaction_allowed":True,
      "as_of":"2026-11-28","expires":"2026-11-29","data_epoch":1}
PHASES=[
 ("initial",{}, "v1", [("public","allow"),("internal","redact"),("restricted","deny"),("internal","redact")]),
 ("policy_change",{"policy_epoch":2,"redaction_allowed":False},"v1",[("public","allow"),("internal","deny"),("restricted","deny"),("internal","deny")]),
 ("revoke",{"grant_epoch":2,"granted":False},"v1",[("public","deny"),("internal","deny"),("restricted","deny"),("public","deny")]),
 ("regrant",{"grant_epoch":3,"role":"staff"},"v1",[("public","allow"),("internal","allow"),("restricted","deny"),("internal","allow")]),
 ("expiry",{"grant_epoch":3,"as_of":"2026-11-30"},"v1",[("public","refresh"),("internal","refresh"),("restricted","refresh"),("public","refresh")]),
 ("renew",{"grant_epoch":4,"expires":"2026-12-01","as_of":"2026-11-30"},"v1",[("public","allow"),("internal","redact"),("restricted","deny"),("internal","redact")]),
 ("rollback",{"grant_epoch":4,"policy_epoch":3},"v1",[("public","allow"),("internal","redact"),("restricted","deny"),("internal","redact")]),
 ("data_change",{"grant_epoch":4,"policy_epoch":3,"data_epoch":2},"v1",[("restricted","deny"),("public","allow"),("internal","redact"),("public","allow")]),
 ("adapter_change",{"grant_epoch":4,"policy_epoch":3,"data_epoch":2},"v2",[("restricted","deny"),("public","allow"),("internal","redact"),("public","allow")]),
 ("tenant_change",{"tenant":"beta","grant_epoch":4,"policy_epoch":3,"data_epoch":2},"v2",[("restricted","deny"),("public","allow"),("internal","redact"),("public","allow")]),
 ("principal_change",{"tenant":"beta","principal":"u2","grant_epoch":4,"policy_epoch":3,"data_epoch":2},"v2",[("restricted","deny"),("public","allow"),("internal","redact"),("public","allow")]),
]
def cases():
    rows=[]
    for phase,changes,version,labels in PHASES:
        for i,(classification,expected) in enumerate(labels):
            # Identical document IDs across phases exercise data and authority changes.
            work={"document":{"id":f"doc-{i}","classification":classification},"brief":dict(BASE,**changes)}
            rows.append((phase,i==0,version,work,expected))
        rows.append((phase,False,*rows[-1][2:]))
    return rows

class Manual:
    def __init__(self,adapter):
        self.adapter=adapter
        self.cache={}
    def run(self,work):
        out={}; hits=[]
        for n in NODES:
            payload={"instruction":n.instruction,"quality_contract":{},
                     "workload":deepcopy(work) if not n.deps else {"brief":deepcopy(work["brief"])},
                     "dependencies":{d:deepcopy(out[d]) for d in n.deps}}
            key=canonical([n.id,n.instruction,n.tier,n.deps,n.max_tokens,n.output_schema,self.adapter.cache_identity(),payload])
            reused=key in self.cache
            if reused:
                value=deepcopy(self.cache[key])
            else:
                value=self.adapter.run(task_id=n.id,input=payload,budget={"max_tokens":n.max_tokens,"max_time_ms":120000},output_schema=n.output_schema)["output"]
            Draft202012Validator(n.output_schema).validate(value)
            if not reused and len(self.cache)<256:
                self.cache[key]=deepcopy(value)
            out[n.id]=value
            hits.append(reused)
        return out["notice"],hits

def run(rounds=30):
    arms=["no_reuse","whole_request_cache","manual_node_cache","kora_node_cache"]
    rows=cases()
    result={a:{"calls":Counter(),"latencies":[],"matches":0,"boundary_checks":0,"hits":0,"model_calls":0,"counter_checks":0} for a in arms}
    for i in range(rounds):
        for arm in arms[i%4:]+arms[:i%4]:
            adapter=Fixture()
            runner=WorkloadEconomicsRunner(nodes=NODES,adapters={"fixture":adapter})
            policy=ExecutionPolicy(arm,{"routine":"fixture"},exact_reuse=(arm=="kora_node_cache"),context_mode="brief+deps")
            manual=Manual(adapter); whole={}
            r=result[arm]
            for phase,first,version,work,expected in rows:
                adapter.version=version
                before=sum(adapter.calls.values())
                start=perf_counter_ns()
                if arm=="manual_node_cache":
                    output,hits=manual.run(work)
                elif arm=="whole_request_cache" and (key:=canonical([version,work])) in whole:
                    output=deepcopy(whole[key]); hits=[True]*3
                else:
                    e=runner.run(workload=work,policy=policy)
                    output=e["output"]; hits=[x["reused"] for x in e["events"]]
                    assert e["adapter_attempts"]==sum(adapter.calls.values())-before
                    assert e["model_calls"]==0
                    r["counter_checks"]+=1
                    if arm=="whole_request_cache": whole[key]=deepcopy(output)
                r["latencies"].append((perf_counter_ns()-start)/1000)
                assert output=={"notice":expected}, (arm,phase,output,expected)
                r["matches"]+=1
                if first:
                    assert not any(hits), (arm,phase,hits)
                    r["boundary_checks"]+=1
                r["hits"]+=sum(hits)
            r["calls"].update(adapter.calls)
    for a,r in result.items():
        times=sorted(r.pop("latencies"))
        r["p50_us"]=statistics.median(times)
        r["p95_us"]=times[(len(times)*95+99)//100-1]
        r["total_calls"]=sum(r["calls"].values())
        assert r["total_calls"]+r["hits"]==r["matches"]*3
    assert result["manual_node_cache"]["total_calls"]==result["kora_node_cache"]["total_calls"]
    return {"scope":"authored synthetic read-only document policy; no document content, no providers","rounds":rounds,"cases_per_round":len(rows),"phases":len(PHASES),"arms":result}
if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
