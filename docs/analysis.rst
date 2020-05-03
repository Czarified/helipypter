Analysis With heliPypter
========================

Using heliPypter, performance for a traditional helicopter with single main and tail rotors can be evaluated.
The first step is defining all the inputs (there are many). The details of all inputs are fully documented on
the `API page <https://helipypter.readthedocs.io/en/latest/api.html>`_.

Units are important, so make sure they are all Imperial!
Metric and automated units with `Pint <https://pint.readthedocs.io/en/0.10.1/>`_ may be supported in a future release.
If you want it, post on the `issues <https://github.com/Czarified/helipypter/issues>`_ page.

The Helicopter class takes numeric weight values for fuel, and a single lumped value for all other masses. It then 
adds the remaining fuel weight and empty mass whenver you call the heli.GW property. Let's use an empty weight fraction
to generate this helicopter.

.. code-block:: python

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

   heli = vh.Helicopter(name='Documentation Helicopter Spec',
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

The Helicopter class has many default values. Some aren't shown here, so it's always good idea to check the
vehicle definition using a simple print function.

.. code-block:: python

    print(heli)

    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
        Documentation Helicopter Spec        
    Rotors: ('MR', 'TR')
    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
    Main Rotor Inputs:
               MR_dia:  35.000 [ft]
                 MR_b:   4.000 []
                MR_ce:  10.400 [in]
             MR_Omega:  43.200 [rad/s]
               MR_cd0:   0.008 []
                 MR_R:  17.500 []
                 MR_A: 962.113 []
              MR_vtip: 756.000 []
               MR_sol:   0.063 []
    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
    Tail Rotor Inputs:
               TR_dia:   5.420 [ft]
                 TR_b:   4.000 []
                TR_ce:   7.000 [in]
             TR_Omega: 239.850 [rad/s]
               TR_cd0:   0.015 []
                 TR_R:   2.710 []
                 TR_A:  23.072 []
              TR_vtip: 649.993 []
               TR_sol:   0.274 []
    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
    Airframe Data:
             GW_empty: 2853.000 [lbs]
              GW_fuel: 869.000 [lbs]
           GW_payload: 1278.000 [lbs]
             download:   0.030 [.%]
          HIGE_factor:   1.200 []
                   fe:  12.900 [ft2]
               l_tail:  21.210 [ft]
                 S_vt:  20.920 [ft2]
                cl_vt:   0.220 []
                AR_vt:   3.000 []
    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
    Engine Data:
           eta_MRxsmn:   0.985 [.%]
           eta_TRxsmn:   0.971 [.%]
          eta_xsmn_co:   0.986 [.%]
             eta_inst:   0.950 [.%]
             xsmn_lim: 674.000 [hp]
              pwr_lim: 813.000 [hp]
    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-

The heli object can now be called to hover, burn fuel, idle, lookup engine power, or fly. However, before we
can perform any flight maneuvers, atmospheric properties must be supplied. Here, we create an Environment class.
For example, to create a Sea-level standard atmosphere and hover at it:

.. code-block:: python

    atm = vh.Environment(alt=0)

    output = heli.HOGE(atm)
    print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
    print('{:^45}'.format('Results - HOGE'))
    print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
    for k,v in doc_chopper.HOGE(atm).items():
        print('{:>17}:  {:>7.4}'.format(k, v))


Hover Out of Ground Effect (HOGE) returns dictionary of the flight point predictions. Sometimes, dictionary output isn't
the easiest to read, even though it's easy to lookup. So we created a simple loop to print the data.

.. code-block:: python

    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
               Results - HOGE
    -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
                    a:    5.717
              delta_0:  0.009518
                   Ct:  0.003937
            TR_thrust:    291.1
                 Cq_i:  0.0001787
                 Cq_v:      0.0
                 Cq_0:  7.502e-05
                 Cq_1:  -1.037e-05
                 Cq_2:  1.317e-05
                   Cq:  0.0002565
                    Q:  6.174e+03
                 P_MR:  2.425e+05
                HP_MR:    485.0
                HP_TR:     45.3
              SHP_ins:    566.0
            SHP_unins:    595.8
                  sfc:   0.4982

WIP...