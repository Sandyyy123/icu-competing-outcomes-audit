import unittest
from competing_outcomes import Record,cumulative_incidence,naive_discharge_probability,demo

class OutcomeTests(unittest.TestCase):
    def test_known_contrast(self):
        d=demo()
        self.assertAlmostEqual(d["final_discharge_CIF"],.5)
        self.assertAlmostEqual(d["naive_death_censored_one_minus_KM"],2/3)
    def test_no_censor_matches_proportions(self):
        r=[Record("a",1,"death"),Record("b",2,"discharge"),Record("c",2,"discharge")]
        x=cumulative_incidence(r)[-1]
        self.assertAlmostEqual(x["discharge"],2/3);self.assertAlmostEqual(x["death"],1/3)
    def test_simultaneous_events(self):
        x=cumulative_incidence([Record("a",1,"death"),Record("b",1,"discharge")])[-1]
        self.assertAlmostEqual(x["discharge"],.5);self.assertAlmostEqual(x["death"],.5)
    def test_same_time_censor_stays_in_risk_set(self):
        x=cumulative_incidence([Record("a",1,"death"),Record("b",1,"censor")])[-1]
        self.assertAlmostEqual(x["death"],.5);self.assertAlmostEqual(x["event_free"],.5)
    def test_censor_before_event(self):
        x=cumulative_incidence([Record("a",1,"censor"),Record("b",2,"discharge")])[-1]
        self.assertAlmostEqual(x["discharge"],1)
    def test_all_censored(self):
        x=cumulative_incidence([Record("a",1,"censor"),Record("b",2,"censor")])[-1]
        self.assertEqual((x["discharge"],x["death"],x["event_free"]),(0,0,1))
    def test_permutation_invariance(self):
        r=[Record("a",1,"death"),Record("b",2,"discharge"),Record("c",3,"censor")]
        self.assertEqual(cumulative_incidence(r),cumulative_incidence(r[::-1]))
    def test_partition_and_monotonicity(self):
        x=demo()["estimates"]
        for row in x:self.assertAlmostEqual(sum(row[k] for k in ["discharge","death","event_free"]),1)
        for a,b in zip(x,x[1:]):
            self.assertGreaterEqual(b["discharge"],a["discharge"])
            self.assertGreaterEqual(b["death"],a["death"])
            self.assertLessEqual(b["event_free"],a["event_free"])
    def test_invalid_inputs(self):
        for rows in [[],[Record("a",-1,"death")],[Record("a",float("nan"),"death")],
                     [Record("a",1,"unknown")],[Record("a",True,"death")],
                     [Record("a",1,"death"),Record("a",2,"discharge")]]:
            with self.subTest(rows=rows),self.assertRaises(ValueError):cumulative_incidence(rows)
    def test_time_zero_and_final_event(self):
        x=cumulative_incidence([Record("a",0,"discharge"),Record("b",1,"death")])
        self.assertAlmostEqual(x[0]["discharge"],.5)
        self.assertAlmostEqual(x[-1]["event_free"],0)
if __name__=="__main__":unittest.main()
