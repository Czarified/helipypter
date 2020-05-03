import helipypter.vehicles as vh
   
# Empty weight fraction
EW_frac = 0.528
# Total Gross Weight
GW_total = 5000
# Crew Weight
w_crew = 200
# Trapped Fluids
w_fluids = 13

w_empty = EW_frac*GW_total + w_crew + w_fluids
# Our payload is 6 people @ 213 lbs each
w_payload = 6*213
w_fuel = GW_total - w_empty - w_payload

doc_chopper = vh.Helicopter(name='Documentation Helicopter Spec',
                MR_dia = 35,
                MR_b = 4,
                MR_ce = 10.4,
            MR_Omega = 43.2,
                MR_cd0 = 0.0080,
                TR_dia = 5.42,
                TR_b = 4,
                TR_ce = 7,
            TR_Omega = 239.85,
                TR_cd0 = 0.015,
            GW_empty = w_empty,
                GW_fuel = w_fuel,
            GW_payload = w_payload,
            download = 0.03,
                    fe = 12.9,
                l_tail = 21.21,
                S_vt = 20.92,
                cl_vt = 0.22,
                AR_vt = 3
                    )

atm = vh.Environment(0)
output = doc_chopper.HOGE(atm)
print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
print('{:^45}'.format('Results - HOGE'))
print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
for k,v in doc_chopper.HOGE(atm).items():
    print('{:>17}:  {:>7.4}'.format(k, v))