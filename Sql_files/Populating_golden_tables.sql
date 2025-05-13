--------------------Creating Golden Tables---------------------------------
INSERT INTO golden.drugevent_patient_golden (report_id,P0,P1,P2)
    SELECT 
            de.report_id,
            concat('This report was produced on ', ISNULL(de.receivedate, 'an unkown date')) AS P0,
            concat(
            CASE WHEN dep.patientagegroup = 1 THEN 'Patient was a neonatal '
                WHEN dep.patientagegroup = 2 THEN 'Patient was a newborn '
                WHEN dep.patientagegroup = 3 THEN 'Patient was an infant '
                WHEN dep.patientagegroup = 4 THEN 'Patient was a child '
                WHEN dep.patientagegroup = 5 THEN 'Patient was an adolescent '
                WHEN dep.patientagegroup = 6 THEN 'Patient was an Adult '
                WHEN dep.patientagegroup = 7 THEN 'Patient was an Elderly '
                ELSE 'Patient was from an unkown age group '
                END,
            CASE WHEN dep.patientsex = 1 THEN 'MALE '
                WHEN dep.patientsex = 2 THEN 'FEMALE '
                WHEN dep.patientsex = 3 THEN 'UNKNOWN GENDER '
                ELSE 'unkown gender '
                END, 
            CASE WHEN dep.patientonsetageunit = 800 THEN concat('age ', dep.patientonsetage * 10, ' years. ')
                WHEN dep.patientonsetageunit = 801 THEN concat('age ', dep.patientonsetage, ' years. ')
                WHEN dep.patientonsetageunit = 802 THEN concat('age ', dep.patientonsetage, ' months. ')
                WHEN dep.patientonsetageunit = 803 THEN concat('age ', dep.patientonsetage, ' weeks. ')  
                WHEN dep.patientonsetageunit = 804 THEN concat('age ', dep.patientonsetage * 10, ' days. ')
                WHEN dep.patientonsetageunit = 805 THEN concat('age ', dep.patientonsetage * 10, ' hours. ')
                ELSE 'unknown age. '
                END
            ) AS P1,
            CASE WHEN dep.patientweight IS NOT NULL THEN concat('Patient weight in Kilograms was ', dep.patientweight) 
                ELSE 'Patient weight was not recorded ' 
                END AS P2
        FROM drugevent de 
        LEFT JOIN drugevent_patient dep ON de.report_id = dep.report_id ;


INSERT INTO golden.drugevent_drug_ofda_golden (report_id,S13,S14)
    SELECT 
            dedo.report_id,
            concat('The substance name of the drug is ',  ISNULL(dedo.substance_name,'unkown')) AS S13,
            concat('The UNII of the drug is ', ISNULL(dedo.unii, 'unkown')) AS S14
    FROM drugevent_drug_ofda dedo;


INSERT INTO golden.drugevent_drug_golden (report_id,S1,S2,S3,S4,S5,S6,S7,S9,S10,S11)
    SELECT 
            ded.report_id,
            CASE WHEN ded.medicinalproduct IS NOT NULL THEN concat('The patient was given a drug whose valid trade name or the generic name is ', ded.medicinalproduct) 
            ELSE 'The patient was given a drug whose valid trade name or the generic name was not recorded ' 
            END AS S1,
            CASE WHEN  ded.drugstartdate IS NOT NULL THEN concat('The start date of drug administration was ', ded.drugstartdate) 
                ELSE  'The start date of drug administration was not recorded ' 
                END  AS S2,
            CASE WHEN ded.drugstartdate IS NOT NULL THEN concat('The patient stopped taking the drug on ', ded.drugstartdate) 
                ELSE 'The date or year when the patient stopped taking the drug was not recorded '
                END  AS S3,
            CASE WHEN ded.activesubstancename IS NOT NULL THEN concat('The active substance in the drug is ', ded.activesubstancename) 
                ELSE 'The active substance in the drug was not recorded'
                END AS S4,
            CASE WHEN ded.drugdosagetext IS NOT NULL THEN concat('Additional detail about the dosage taken or schedule of administration is ', ded.drugdosagetext)
                ELSE 'No additional details about the drug was recorded in the report'
                END AS S5,
            CASE WHEN ded.drugindication IS NOT NULL THEN concat('Indication for the drug use says ', ded.drugindication) 
                ELSE 'NO Indication for the drug on the package'
                END   AS S6,
            CASE WHEN ded.drugseparatedosagenumb IS NOT NULL THEN concat('And the patient was given ', ded.drugseparatedosagenumb, ' number of separate doses.')
                ELSE 'The number of doses given to the patient are unknown'
                END  AS S7,
            concat('A total dose of ', ISNULL(drugcumulativedosagenumb,'unkown '), 
            CASE WHEN ded.drugcumulativedosageunit = '001' THEN ' kilograms'
                WHEN ded.drugcumulativedosageunit = '002' THEN ' grams'
                WHEN ded.drugcumulativedosageunit = '003' THEN ' milligrams'
                WHEN ded.drugcumulativedosageunit = '004' THEN ' micrograms'
                ELSE 'amount'
                END, ' was administered to the patient until the first reaction was experienced.'
            ) AS S9,
            concat(
            CASE WHEN ded.actiondrug = 1 THEN 'After the reactions, Drug was withdrawn '
                WHEN ded.actiondrug = 2 THEN 'After the reactions, Dose was reduced '
                WHEN ded.actiondrug = 3 THEN 'After the reactions, Dose was increased '
                WHEN ded.actiondrug = 4 THEN 'After the reactions, Drug was not changed '
                ELSE '' END, 
            CASE WHEN ded.drugadditional = 1 THEN 'and the reactions abated.'
                WHEN ded.drugadditional = 2 THEN 'and the reactions did not abate.'
                ELSE '' END 
            ) AS S10,
            CASE WHEN ded.drugcharacterization = 1 THEN 'Suspect - the drug was considered to be the cause of the reactions'
                WHEN ded.drugcharacterization = 2 THEN 'Concomitant - the drug was reported as being taken along with the suspect drug'
                WHEN ded.drugcharacterization = 3 THEN 'Interacting - the drug was considered by the reporter to have interacted with the suspect drug'
                ELSE ''
                END AS S11
    FROM drugevent_drug ded

INSERT INTO golden.drugevent_reaction (report_id,S8,S12)
    SELECT 
            der.report_id,
            CASE WHEN der.reactionmeddrapt IS NOT NULL THEN concat('The patient started showing the reaction ', der.reactionmeddrapt) 
                 ELSE 'The reactions patient started were not recorded '
                 END AS S8,
            CASE WHEN der.reactionoutcome = 1 THEN 'Patient recovered from the reaction or reaction resolved at the time of filing this report'
                WHEN der.reactionoutcome = 2 THEN 'Patient recovering from the reaction or reaction resolving at the time of filing this report'
                WHEN der.reactionoutcome = 3 THEN 'Patient did not recover from the reaction or reaction did not resolve at the time of filing this report'
                WHEN der.reactionoutcome = 4 THEN 'Patient recovered/resolved with sequelae (consequent health issues) at the time of filing this report' 
                WHEN der.reactionoutcome = 5 THEN 'Patient died from the reaction or reaction'
                ELSE ''
                END AS S12
    FROM drugevent_reaction der;


INSERT INTO golden.drugevent_golden (report_id,S15,S16,S17,S18,S19,S20,S21)
    SELECT 
            de.report_id,
            CASE WHEN de.serious = 1 THEN 'The adverse event resulted in death, a life threatening condition, hospitalization, disability, congenital anomaly, or other serious condition'
                WHEN de.serious = 2 THEN 'The adverse event did not result in death, a life threatening condition, hospitalization, disability, congenital anomaly, or other serious condition'
                ELSE '' END AS S15,
            CASE WHEN de.seriousnesscongenitalanomali = 1 THEN 'The adverse event resulted in serious congenital anomaly'
                ELSE '' END AS S16, 
            CASE WHEN de.seriousnessdeath = 1 THEN 'The adverse event resulted in death'
                ELSE '' END AS S17, 
            CASE WHEN de.seriousnessdisabling = 1 THEN 'The adverse event resulted in disability'
                ELSE '' END AS S18,
            CASE WHEN de.seriousnesshospitalization = 1 THEN 'The adverse event resulted in hospitalization'
                ELSE '' END AS S19,
            CASE WHEN de.seriousnesslifethreatening = 1 THEN 'The adverse event resulted in life threatening condition'
                ELSE '' END AS S20,
            CASE WHEN de.seriousnessother = 1 THEN 'The adverse event resulted in other serious conditions'
                ELSE '' END AS S21
    FROM drugevent de;

INSERT INTO golden.final_golden(report_id,text)
SELECT
    de.report_id, concat(P0,'. ',P1,' ',P2,'. ',S012,'. ',S1321,'. ') 
FROM golden.S012 de
inner JOIN  golden.S1321 ded ON de.report_id = ded.report_id
inner JOIN  golden.drugevent_patient_golden dep ON de.report_id = dep.report_id;
