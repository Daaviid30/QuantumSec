# QuantumSec thesis campaign report

## Environment

Campaign `thesis-v1.0.1` / preset `smoke`; Python 3.14.7, NumPy 2.5.0, liboqs 0.16.0, OS Windows 11. Git `ac46477bb374bde1c0ace1ef0bcfbc26b199dcfa`; dirty worktree: `True`.

## Methodology

All summaries and figures in this report were regenerated from immutable raw JSON records. Timings use medians and IQRs. Binomial estimates pool exact error/trial counts before applying two-sided Wilson 95% intervals. Warm-ups are discarded. PQC conditions use a fixed randomized order, while QKD seeds follow the manifest policy.

## E1

| profile | n | total_handshake_median_ns | total_handshake_q1_ns | total_handshake_q3_ns | total_handshake_iqr_ns | total_handshake_median_ms | ml_kem_keygen_median_ns | ml_kem_keygen_q1_ns | ml_kem_keygen_q3_ns | ml_kem_keygen_iqr_ns | ml_kem_keygen_median_ms | hqc_keygen_median_ns | hqc_keygen_q1_ns | hqc_keygen_q3_ns | hqc_keygen_iqr_ns | hqc_keygen_median_ms | server_offer_sign_median_ns | server_offer_sign_q1_ns | server_offer_sign_q3_ns | server_offer_sign_iqr_ns | server_offer_sign_median_ms | server_offer_verify_median_ns | server_offer_verify_q1_ns | server_offer_verify_q3_ns | server_offer_verify_iqr_ns | server_offer_verify_median_ms | ml_kem_encapsulate_median_ns | ml_kem_encapsulate_q1_ns | ml_kem_encapsulate_q3_ns | ml_kem_encapsulate_iqr_ns | ml_kem_encapsulate_median_ms | hqc_encapsulate_median_ns | hqc_encapsulate_q1_ns | hqc_encapsulate_q3_ns | hqc_encapsulate_iqr_ns | hqc_encapsulate_median_ms | client_exchange_sign_median_ns | client_exchange_sign_q1_ns | client_exchange_sign_q3_ns | client_exchange_sign_iqr_ns | client_exchange_sign_median_ms | client_exchange_verify_median_ns | client_exchange_verify_q1_ns | client_exchange_verify_q3_ns | client_exchange_verify_iqr_ns | client_exchange_verify_median_ms | ml_kem_decapsulate_median_ns | ml_kem_decapsulate_q1_ns | ml_kem_decapsulate_q3_ns | ml_kem_decapsulate_iqr_ns | ml_kem_decapsulate_median_ms | hqc_decapsulate_median_ns | hqc_decapsulate_q1_ns | hqc_decapsulate_q3_ns | hqc_decapsulate_iqr_ns | hqc_decapsulate_median_ms | transcript_construction_hash_median_ns | transcript_construction_hash_q1_ns | transcript_construction_hash_q3_ns | transcript_construction_hash_iqr_ns | transcript_construction_hash_median_ms | kem_combiner_encoding_median_ns | kem_combiner_encoding_q1_ns | kem_combiner_encoding_q3_ns | kem_combiner_encoding_iqr_ns | kem_combiner_encoding_median_ms | hkdf_session_median_ns | hkdf_session_q1_ns | hkdf_session_q3_ns | hkdf_session_iqr_ns | hkdf_session_median_ms | hkdf_confirmation_median_ns | hkdf_confirmation_q1_ns | hkdf_confirmation_q3_ns | hkdf_confirmation_iqr_ns | hkdf_confirmation_median_ms | finished_generation_median_ns | finished_generation_q1_ns | finished_generation_q3_ns | finished_generation_iqr_ns | finished_generation_median_ms | finished_verification_median_ns | finished_verification_q1_ns | finished_verification_q3_ns | finished_verification_iqr_ns | finished_verification_median_ms | kem_public_key_bytes_median | kem_ciphertext_bytes_median | signature_bytes_median | finished_bytes_median | canonical_protocol_bytes_median | transcript_bytes_median | public_key_provisioning_bytes_median | serialized_transport_bytes | pqc_alice_identity_generation_time_ns | pqc_bob_identity_generation_time_ns | pqc_total_identity_generation_time_ns | pqc_public_identity_bytes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PQC-DIVERSE | 1 | 86461000.0 | 86461000.0 | 86461000.0 | 0.0 | 86.461 | 407900.0 | 407900.0 | 407900.0 | 0.0 | 0.4079 | 12940100.0 | 12940100.0 | 12940100.0 | 0.0 | 12.9401 | 2225800.0 | 2225800.0 | 2225800.0 | 0.0 | 2.2258 | 894100.0 | 894100.0 | 894100.0 | 0.0 | 0.8941 | 338300.0 | 338300.0 | 338300.0 | 0.0 | 0.3383 | 26090900.0 | 26090900.0 | 26090900.0 | 0.0 | 26.0909 | 1348600.0 | 1348600.0 | 1348600.0 | 0.0 | 1.3486 | 883800.0 | 883800.0 | 883800.0 | 0.0 | 0.8838 | 346500.0 | 346500.0 | 346500.0 | 0.0 | 0.3465 | 40224400.0 | 40224400.0 | 40224400.0 | 0.0 | 40.2244 | 360400.0 | 360400.0 | 360400.0 | 0.0 | 0.3604 | 21300.0 | 21300.0 | 21300.0 | 0.0 | 0.0213 | 54000.0 | 54000.0 | 54000.0 | 0.0 | 0.054 | 29000.0 | 29000.0 | 29000.0 | 0.0 | 0.029 | 41100.0 | 41100.0 | 41100.0 | 0.0 | 0.0411 | 27000.0 | 27000.0 | 27000.0 | 0.0 | 0.027 | 5698.0 | 10066.0 | 6618.0 | 96.0 | 16105.0 | 22852.0 | 3904.0 | None | 858400.0 | 668600.0 | 1527000.0 | 3904.0 |
| PQC-BASE | 1 | 12765100.0 | 12765100.0 | 12765100.0 | 0.0 | 12.7651 | 308500.0 | 308500.0 | 308500.0 | 0.0 | 0.3085 | None |  |  | None |  | 6613000.0 | 6613000.0 | 6613000.0 | 0.0 | 6.613 | 791300.0 | 791300.0 | 791300.0 | 0.0 | 0.7913 | 312700.0 | 312700.0 | 312700.0 | 0.0 | 0.3127 | None |  |  | None |  | 3066500.0 | 3066500.0 | 3066500.0 | 0.0 | 3.0665 | 766000.0 | 766000.0 | 766000.0 | 0.0 | 0.766 | 347900.0 | 347900.0 | 347900.0 | 0.0 | 0.3479 | None |  |  | None |  | 189600.0 | 189600.0 | 189600.0 | 0.0 | 0.1896 | 15400.0 | 15400.0 | 15400.0 | 0.0 | 0.0154 | 52500.0 | 52500.0 | 52500.0 | 0.0 | 0.0525 | 27400.0 | 27400.0 | 27400.0 | 0.0 | 0.0274 | 39100.0 | 39100.0 | 39100.0 | 0.0 | 0.0391 | 24900.0 | 24900.0 | 24900.0 | 0.0 | 0.0249 | 1184.0 | 1088.0 | 6618.0 | 96.0 | 2585.0 | 9332.0 | 3904.0 | None | 858400.0 | 668600.0 | 1527000.0 | 3904.0 |

Operation medians are direct narrow measurements. Their sum is not necessarily the median total handshake.

## E2

| condition_id | channel | parameters_json | n_runs | z_errors | z_trials | z_estimate | z_lower | z_upper | x_errors | x_trials | x_estimate | x_lower | x_upper | aggregate_errors | aggregate_trials | aggregate_estimate | aggregate_lower | aggregate_upper | theory_z | theory_x | theory_aggregate | absolute_error_z | absolute_error_x | absolute_error_aggregate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| identity | identity | {"type": "identity"} | 1 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 0 | 50 | 0.0 | 0.0 | 0.07134759913335868 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| depolarizing-0.02 | depolarizing | {"p": 0.02, "type": "depolarizing"} | 1 | 0 | 23 | 0.0 | 0.0 | 0.14311661845042678 | 0 | 29 | 0.0 | 0.0 | 0.11696979849974071 | 0 | 52 | 0.0 | 0.0 | 0.0687922361238623 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| depolarizing-0.05 | depolarizing | {"p": 0.05, "type": "depolarizing"} | 1 | 1 | 26 | 0.038461538461538464 | 0.006821984993543487 | 0.18892778903034751 | 0 | 24 | 0.0 | 0.0 | 0.13797620467498012 | 1 | 50 | 0.02 | 0.0035392592716462293 | 0.1049544358963781 | 0.025 | 0.025 | 0.025 | 0.013461538461538462 | 0.025 | 0.005000000000000001 |
| depolarizing-0.10 | depolarizing | {"p": 0.1, "type": "depolarizing"} | 1 | 1 | 28 | 0.03571428571428571 | 0.0063325198490377516 | 0.17712197743353314 | 1 | 25 | 0.04 | 0.007096233501987251 | 0.19544063736193729 | 2 | 53 | 0.03773584905660377 | 0.010410287275826845 | 0.12754287197418354 | 0.05 | 0.05 | 0.05 | 0.01428571428571429 | 0.010000000000000002 | 0.01226415094339623 |
| depolarizing-0.15 | depolarizing | {"p": 0.15, "type": "depolarizing"} | 1 | 1 | 25 | 0.04 | 0.007096233501987251 | 0.19544063736193729 | 1 | 25 | 0.04 | 0.007096233501987251 | 0.19544063736193729 | 2 | 50 | 0.04 | 0.011038884327619819 | 0.13460090687507018 | 0.075 | 0.075 | 0.075 | 0.034999999999999996 | 0.034999999999999996 | 0.034999999999999996 |
| depolarizing-0.20 | depolarizing | {"p": 0.2, "type": "depolarizing"} | 1 | 0 | 28 | 0.0 | 0.0 | 0.12064330476584559 | 4 | 25 | 0.16 | 0.0640345145667644 | 0.3465362160717885 | 4 | 53 | 0.07547169811320754 | 0.0297395550869467 | 0.17858477483653223 | 0.1 | 0.1 | 0.1 | 0.1 | 0.06 | 0.02452830188679246 |
| depolarizing-0.25 | depolarizing | {"p": 0.25, "type": "depolarizing"} | 1 | 1 | 27 | 0.037037037037037035 | 0.006568145980785131 | 0.18283465933575843 | 3 | 25 | 0.12 | 0.041668171504403634 | 0.2995579392092732 | 4 | 52 | 0.07692307692307693 | 0.030319345184930138 | 0.18173562384295333 | 0.125 | 0.125 | 0.125 | 0.08796296296296297 | 0.0050000000000000044 | 0.04807692307692307 |
| bit-flip-0.02 | bit_flip | {"p": 0.02, "type": "bit_flip"} | 1 | 0 | 24 | 0.0 | 0.0 | 0.13797620467498012 | 0 | 26 | 0.0 | 0.0 | 0.12872892185921525 | 0 | 50 | 0.0 | 0.0 | 0.07134759913335868 | 0.02 | 0.0 | 0.01 | 0.02 | 0.0 | 0.01 |
| bit-flip-0.05 | bit_flip | {"p": 0.05, "type": "bit_flip"} | 1 | 2 | 25 | 0.08 | 0.02222040128484759 | 0.2496610895039531 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 2 | 50 | 0.04 | 0.011038884327619819 | 0.13460090687507018 | 0.05 | 0.0 | 0.025 | 0.03 | 0.0 | 0.015 |
| bit-flip-0.10 | bit_flip | {"p": 0.1, "type": "bit_flip"} | 1 | 3 | 26 | 0.11538461538461539 | 0.04003244623610615 | 0.2897590321171364 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 3 | 51 | 0.058823529411764705 | 0.020206639422464673 | 0.1592462604880042 | 0.1 | 0.0 | 0.05 | 0.015384615384615385 | 0.0 | 0.008823529411764702 |
| bit-flip-0.16 | bit_flip | {"p": 0.16, "type": "bit_flip"} | 1 | 5 | 27 | 0.18518518518518517 | 0.08180707142976532 | 0.36698683618548433 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 5 | 52 | 0.09615384615384616 | 0.04177435105257249 | 0.20609630120131628 | 0.16 | 0.0 | 0.08 | 0.02518518518518517 | 0.0 | 0.016153846153846158 |
| bit-flip-0.20 | bit_flip | {"p": 0.2, "type": "bit_flip"} | 1 | 9 | 27 | 0.3333333333333333 | 0.18643261498715652 | 0.5217523949267993 | 0 | 29 | 0.0 | 0.0 | 0.11696979849974071 | 9 | 56 | 0.16071428571428573 | 0.0869266760759514 | 0.2780620666974952 | 0.2 | 0.0 | 0.1 | 0.1333333333333333 | 0.0 | 0.06071428571428572 |
| phase-flip-0.02 | phase_flip | {"p": 0.02, "type": "phase_flip"} | 1 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 3 | 30 | 0.1 | 0.03459988874733419 | 0.25621082579184085 | 3 | 55 | 0.05454545454545454 | 0.018723215554684494 | 0.14853060544053787 | 0.0 | 0.02 | 0.01 | 0.0 | 0.08 | 0.04454545454545454 |
| phase-flip-0.05 | phase_flip | {"p": 0.05, "type": "phase_flip"} | 1 | 0 | 26 | 0.0 | 0.0 | 0.12872892185921525 | 1 | 31 | 0.03225806451612903 | 0.005717221525416816 | 0.16194105164724903 | 1 | 57 | 0.017543859649122806 | 0.003103664651408093 | 0.09290749178567684 | 0.0 | 0.05 | 0.025 | 0.0 | 0.01774193548387097 | 0.007456140350877195 |
| phase-flip-0.10 | phase_flip | {"p": 0.1, "type": "phase_flip"} | 1 | 0 | 26 | 0.0 | 0.0 | 0.12872892185921525 | 4 | 25 | 0.16 | 0.0640345145667644 | 0.3465362160717885 | 4 | 51 | 0.0784313725490196 | 0.03092219678848919 | 0.18499946312595883 | 0.0 | 0.1 | 0.05 | 0.0 | 0.06 | 0.028431372549019604 |
| phase-flip-0.16 | phase_flip | {"p": 0.16, "type": "phase_flip"} | 1 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 4 | 24 | 0.16666666666666666 | 0.06678676328632951 | 0.3585307064969906 | 4 | 49 | 0.08163265306122448 | 0.03220281766776367 | 0.19189127596571287 | 0.0 | 0.16 | 0.08 | 0.0 | 0.006666666666666654 | 0.0016326530612244816 |
| phase-flip-0.20 | phase_flip | {"p": 0.2, "type": "phase_flip"} | 1 | 0 | 27 | 0.0 | 0.0 | 0.12455502974186704 | 1 | 24 | 0.041666666666666664 | 0.00739345616550581 | 0.20241806478655933 | 1 | 51 | 0.0196078431372549 | 0.0034696926410608397 | 0.10304568726144972 | 0.0 | 0.2 | 0.1 | 0.0 | 0.15833333333333335 | 0.0803921568627451 |
| amplitude-damping-0.02 | amplitude_damping | {"gamma": 0.02, "type": "amplitude_damping"} | 1 | 0 | 27 | 0.0 | 0.0 | 0.12455502974186704 | 0 | 23 | 0.0 | 0.0 | 0.14311661845042678 | 0 | 50 | 0.0 | 0.0 | 0.07134759913335868 | 0.01 | 0.00502525316941671 | 0.007512626584708355 | 0.01 | 0.00502525316941671 | 0.007512626584708355 |
| amplitude-damping-0.05 | amplitude_damping | {"gamma": 0.05, "type": "amplitude_damping"} | 1 | 0 | 24 | 0.0 | 0.0 | 0.13797620467498012 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 0 | 49 | 0.0 | 0.0 | 0.07269781922049635 | 0.025 | 0.012660282759551833 | 0.018830141379775917 | 0.025 | 0.012660282759551833 | 0.018830141379775917 |
| amplitude-damping-0.10 | amplitude_damping | {"gamma": 0.1, "type": "amplitude_damping"} | 1 | 1 | 26 | 0.038461538461538464 | 0.006821984993543487 | 0.18892778903034751 | 0 | 24 | 0.0 | 0.0 | 0.13797620467498012 | 1 | 50 | 0.02 | 0.0035392592716462293 | 0.1049544358963781 | 0.05 | 0.025658350974743116 | 0.03782917548737156 | 0.011538461538461539 | 0.025658350974743116 | 0.01782917548737156 |
| amplitude-damping-0.20 | amplitude_damping | {"gamma": 0.2, "type": "amplitude_damping"} | 1 | 2 | 25 | 0.08 | 0.02222040128484759 | 0.2496610895039531 | 0 | 26 | 0.0 | 0.0 | 0.12872892185921525 | 2 | 51 | 0.0392156862745098 | 0.010821083352867099 | 0.13216305655362262 | 0.1 | 0.05278640450004207 | 0.07639320225002104 | 0.020000000000000004 | 0.05278640450004207 | 0.037177515975511236 |
| amplitude-damping-0.30 | amplitude_damping | {"gamma": 0.3, "type": "amplitude_damping"} | 1 | 6 | 26 | 0.23076923076923078 | 0.11033849405783294 | 0.42051554078943687 | 1 | 28 | 0.03571428571428571 | 0.0063325198490377516 | 0.17712197743353314 | 7 | 54 | 0.12962962962962962 | 0.0642372074732626 | 0.24421730222369764 | 0.15 | 0.08166998673296222 | 0.1158349933664811 | 0.08076923076923079 | 0.045955701018676506 | 0.013794636263148516 |
| pauli-symmetric | pauli | {"px": 0.02, "py": 0.02, "pz": 0.02, "type": "pauli"} | 1 | 1 | 25 | 0.04 | 0.007096233501987251 | 0.19544063736193729 | 2 | 26 | 0.07692307692307693 | 0.021355088472276226 | 0.24141553771629054 | 3 | 51 | 0.058823529411764705 | 0.020206639422464673 | 0.1592462604880042 | 0.04 | 0.04 | 0.04 | 0.0 | 0.036923076923076927 | 0.018823529411764704 |
| pauli-x-dominant | pauli | {"px": 0.08, "py": 0.01, "pz": 0.02, "type": "pauli"} | 1 | 2 | 23 | 0.08695652173913043 | 0.024180004484220377 | 0.2679598107574366 | 0 | 28 | 0.0 | 0.0 | 0.12064330476584559 | 2 | 51 | 0.0392156862745098 | 0.010821083352867099 | 0.13216305655362262 | 0.09 | 0.03 | 0.06 | 0.0030434782608695643 | 0.03 | 0.020784313725490194 |
| pauli-z-dominant | pauli | {"px": 0.02, "py": 0.01, "pz": 0.08, "type": "pauli"} | 1 | 0 | 25 | 0.0 | 0.0 | 0.13319225093904843 | 5 | 28 | 0.17857142857142858 | 0.07878501945604274 | 0.3559142478934294 | 5 | 53 | 0.09433962264150944 | 0.040972641497250495 | 0.2025372737629627 | 0.03 | 0.09 | 0.06 | 0.03 | 0.08857142857142858 | 0.03433962264150944 |

This validates the implemented numerical model under tested channel assumptions; it does not prove BB84 security.

## E3

| condition_id | intercept_fraction | n_runs | theory_qber | qber_errors | qber_trials | qber_estimate | qber_lower | qber_upper | abort_errors | abort_trials | abort_estimate | abort_lower | abort_upper | n_final_median | n_final_q1 | n_final_q3 | n_final_iqr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intercept-0.0 | 0.0 | 1 | 0.0 | 0 | 49 | 0.0 | 0.0 | 0.07269781922049635 | 0 | 1 | 0.0 | 0.0 | 0.7934506856227626 | 158.0 | 158.0 | 158.0 | 0.0 |
| intercept-0.1 | 0.1 | 1 | 0.025 | 0 | 53 | 0.0 | 0.0 | 0.06758198857654184 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.2 | 0.2 | 1 | 0.05 | 4 | 52 | 0.07692307692307693 | 0.030319345184930138 | 0.18173562384295333 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.3 | 0.3 | 1 | 0.075 | 8 | 53 | 0.1509433962264151 | 0.07852417850846265 | 0.27054249276195336 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.4 | 0.4 | 1 | 0.1 | 3 | 52 | 0.057692307692307696 | 0.0198141721122706 | 0.15642511368960757 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.5 | 0.5 | 1 | 0.125 | 7 | 49 | 0.14285714285714285 | 0.07096423720406764 | 0.26667706223914406 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.6 | 0.6 | 1 | 0.15 | 12 | 52 | 0.23076923076923078 | 0.13724260925492748 | 0.3613378255809983 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.7 | 0.7 | 1 | 0.175 | 14 | 55 | 0.2545454545454545 | 0.15812114773072916 | 0.38301871281765865 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.8 | 0.8 | 1 | 0.2 | 10 | 51 | 0.19607843137254902 | 0.1101534251246669 | 0.32458079481365604 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-0.9 | 0.9 | 1 | 0.225 | 8 | 54 | 0.14814814814814814 | 0.07703063137605345 | 0.26600115283605885 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| intercept-1.0 | 1.0 | 1 | 0.25 | 17 | 49 | 0.3469387755102041 | 0.2292439283453896 | 0.48688805713027267 | 1 | 1 | 1.0 | 0.20654931437723745 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |

The f/4 relation applies only to the stated ideal random-basis intercept-resend model.

## E4

| profile | n | authentication_executed | authentication_verified | mechanism | trust_assumption | authenticated_bytes_median | authenticated_bytes_iqr | evidence_bytes_median | evidence_bytes_iqr | checkpoints_median | checkpoints_iqr | generation_operations_median | generation_operations_iqr | verification_operations_median | verification_operations_iqr | generation_time_median_ns | generation_time_iqr_ns | verification_time_median_ns | verification_time_iqr_ns | total_time_median_ns | total_time_iqr_ns | secret_bits_consumed_median | secret_bits_consumed_iqr | public_key_provisioning_bytes_median | public_key_provisioning_bytes_iqr | forgery_bound |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QKD-ASSUMED | 1 | False | None | assumed | The classical BB84 channel is assumed authenticated externally. | None | None | None | None | None | None | None | None | None | None | None | None | None | None | None | None | None | None | None | None | None |
| QKD-CLASSICAL-AUTH | 1 | True | True | wegman_carter | Alice and Bob hold identical, uniformly random, pre-shared authentication material; every Toeplitz selector and one-time tag mask is fresh and never reused. | 108718.0 | 0.0 | 32.0 | 0.0 | 2.0 | 0.0 | 2.0 | 0.0 | 2.0 | 0.0 | 142570000.0 | 0.0 | 140791400.0 | 0.0 | 283361400.0 | 0.0 | 870254.0 | 0.0 | None | None | <= 2^-128 per fresh-key checkpoint |
| QKD-PQC-AUTH | 1 | True | True | ml_dsa_65 | Peer ML-DSA-65 public identities are authenticated and pre-provisioned before the QKD session. | 108718.0 | 0.0 | 6618.0 | 0.0 | 2.0 | 0.0 | 2.0 | 0.0 | 2.0 | 0.0 | 7562700.0 | 0.0 | 3140700.0 | 0.0 | 10703400.0 | 0.0 | None | None | 3904.0 | 0.0 | None |

QKD-ASSUMED is NOT EXECUTED, not a zero-cost authentication primitive. The executed mechanisms have different assurance assumptions.

## E5

| profile | n | pqc_crypto_median_ns | pqc_crypto_iqr_ns | hybrid_composition_median_ns | hybrid_composition_iqr_ns | overhead_ratio_median | overhead_ratio_iqr | extra_transmitted_bytes_median | extra_transmitted_bytes_iqr | canonical_combiner_input_bytes_median | canonical_combiner_input_bytes_iqr | encoding_overhead_bytes_median | encoding_overhead_bytes_iqr | public_context_bytes_median | public_context_bytes_iqr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HYBRID-DIVERSE | 1 | 89863400.0 | 0.0 | 278600.0 | 0.0 | 0.0031002610629021383 | 0.0 | 482.0 | 0.0 | 458.0 | 0.0 | 345.0 | 0.0 | 289.0 | 0.0 |
| PQC-BASE | 1 | 9910900.0 | 0.0 | None | None | None | None | None | None | None | None | None | None | None | None |
| PQC-DIVERSE | 1 | 89581100.0 | 0.0 | None | None | None | None | None | None | None | None | None | None | None | None |
| HYBRID | 1 | 11619900.0 | 0.0 | 331200.0 | 0.0 | 0.02850282704670436 | 0.0 | 466.0 | 0.0 | 335.0 | 0.0 | 256.0 | 0.0 | 267.0 | 0.0 |

Hybrid composition excludes BB84 numerical simulation. Local canonical input sizes are not labeled as network traffic; extra transmitted bytes are the two Finished messages.

## D1

AES-256-GCM round trip: `True`. All ciphertext, tag, and AAD mutations rejected: `True`.

## Hypotheses

| hypothesis | status | handshake_delta_ns | hqc_operation_medians_sum_ns | all_theory_points_inside_wilson_95 | maximum_absolute_qber_error | maximum_tested_basis_theory_gap | small_threshold | maximum_median_ratio | executed_profiles_with_positive_cost | d1_integrity_evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | SUPPORTED | 73695900.0 | 79255400.0 |  |  |  |  |  |  |  |
| H2 | QUALIFIED |  |  | False | 0.09693877551020408 |  |  |  |  |  |
| H3 | SUPPORTED |  |  |  |  | 0.2 |  |  |  |  |
| H4 | SUPPORTED |  |  |  |  |  | 0.1 | 0.02850282704670436 |  |  |
| H5 | SUPPORTED |  |  |  |  |  |  |  | True | True |

## Threats to validity

- QKD results are numerical logical-qubit simulations, not physical QKD latency, secret-key rate, fibre throughput, distance, or hardware timing.
- The QKD model omits optical loss, dark counts, decoy states, detector imperfections, and a finite-key composable security proof.
- Eve is limited to intercept-resend; this is not evidence of security against general adversaries.
- PQC timings are specific to the recorded reference hardware/software environment.
- The finite run counts leave sampling uncertainty, reflected where binomial Wilson intervals apply.
- The hybrid construction is not claimed to have a formal robust-combiner proof.

## Limitations

The campaign compares software operations within one environment and preserves unlike timing domains. It makes no universal hardware-performance or cryptographic-superiority claim. Serialized transport size remains N/A where no real transport serialization exists.
