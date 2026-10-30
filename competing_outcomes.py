"""Small synthetic proof for first-event cumulative incidence, not clinical analysis.
Input: one record per person, entry at time 0, right censoring only.
Same-time events precede censoring. No weights, delayed entry, regression or CIs.
"""
from dataclasses import dataclass
import json
import math

@dataclass(frozen=True)
class Record:
    id: str
    time: float
    outcome: str   # discharge | death | censor

def validate(records):
    records=list(records)
    if not records:
        raise ValueError("At least one record is required")
    if len({r.id for r in records}) != len(records):
        raise ValueError("Duplicate person ID")
    for r in records:
        if not isinstance(r.id,str) or not r.id:
            raise ValueError("Nonempty string person ID required")
        if isinstance(r.time,bool) or not isinstance(r.time,(float,int)) or not math.isfinite(r.time) or r.time<0:
            raise ValueError("Finite nonnegative time required")
        if r.outcome not in {"discharge","death","censor"}:
            raise ValueError("Unknown outcome")
    return records

def cumulative_incidence(records):
    """Aalen-Johansen for a single initial state and two absorbing outcomes."""
    records=validate(records)
    survival=1.0
    incidence={"discharge":0.0,"death":0.0}
    rows=[]
    for t in sorted({r.time for r in records}):
        risk=sum(r.time>=t for r in records)
        events={k:sum(r.time==t and r.outcome==k for r in records)
                for k in incidence}
        before=survival
        for k,n in events.items():
            incidence[k]+=before*n/risk
        survival*=1-sum(events.values())/risk
        rows.append({"time":t,"risk":risk,"discharge":incidence["discharge"],
                     "death":incidence["death"],"event_free":survival})
    return rows

def naive_discharge_probability(records):
    """Deliberately wrong probability interpretation: treats death as censoring.
    Included solely as a didactic contrast, not a recommended estimator.
    """
    records=validate(records)
    survival=1.0
    for t in sorted({r.time for r in records}):
        n=sum(r.time>=t for r in records)
        d=sum(r.time==t and r.outcome=="discharge" for r in records)
        survival*=1-d/n
    return 1-survival

def demo():
    records=[Record("synthetic-A",1,"death"),Record("synthetic-B",2,"discharge"),
             Record("synthetic-C",3,"discharge"),Record("synthetic-D",4,"censor")]
    return {"label":"CONSTRUCTED FOUR-PERSON TEACHING FIXTURE, NOT CLIENT DATA",
            "input":[r.__dict__ for r in records],
            "estimates":cumulative_incidence(records),
            "final_discharge_CIF":cumulative_incidence(records)[-1]["discharge"],
            "naive_death_censored_one_minus_KM":naive_discharge_probability(records)}
if __name__=="__main__":
    print(json.dumps(demo(),indent=2))
