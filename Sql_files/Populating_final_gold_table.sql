INSERT INTO golden.drugevent_reaction (report_id,S8)
    SELECT 
            der.report_id,
            CASE WHEN der.reactions IS NOT NULL THEN concat('The patient started showing the reactions ', der.reactions) 
                 ELSE 'The reactions patient started were not recorded '
                 END AS S8
    FROM drugevent_reaction der;

-- CREATE table  golden.drugevent_reaction (report_id bigint, S8 VARCHAR(MAX) )
CREATE table  golden.S111 (report_id bigint, 
                           S111 VARCHAR(MAX), 
                          )

INSERT INTO golden.S111 (report_id,S111)
    SELECT 
            der.report_id,
            CONCAT(S1,'. ',S2,'. ',S3,'. ',S4,'. ',S5,'. ',S6,'. ',S7,'. ',S8,'. ',S9,'. ',S10,'. ',S11, '. ')
    FROM golden.drugevent_reaction der
    INNER JOIN golden.drugevent_drug_golden ded ON   ded.report_id =der.report_id ;

DROP TABLE golden.S111 

DROP TABLE golden.final_golden

CREATE table  golden.final (report_id bigint, 
                            PS VARCHAR(MAX), 
                           )

INSERT INTO golden.final (report_id,PS)
    SELECT 
            der.report_id,
            CONCAT(P0,'. ',P1,'. ',P2,'. ',S111,'. ',S1321,'. ')
    FROM golden.S111 der
    INNER JOIN golden.S1321 ded ON   ded.report_id = der.report_id
    INNER JOIN golden.drugevent_patient_golden dpg  ON dpg.report_id = der.report_id;
select * from golden.final