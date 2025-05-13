-- Databricks notebook source
CREATE CATALOG openfda;
CREATE SCHEMA openfdaraw;

-- COMMAND ----------

DROP TABLE IF EXISTS openfda.openfdaraw.drugevent_raw;
CREATE TABLE IF NOT EXISTS openfda.openfdaraw.drugevent_raw(
  authoritynumb	string,
  companynumb	string,
  duplicate	string,
  fulfillexpeditecriteria	string,
  occurcountry	string,
  patient struct<
    drug:array<struct<
      actiondrug:string,
      activesubstance:struct<activesubstancename:string>,
      drugadditional:string,
      drugadministrationroute:string,
      drugauthorizationnumb:string,
      drugbatchnumb:string,
      drugcharacterization:string,
      drugcumulativedosagenumb:string,
      drugcumulativedosageunit:string,
      drugdosageform:string,
      drugdosagetext:string,
      drugenddate:string,
      drugenddateformat:string,
      drugindication:string,
      drugintervaldosagedefinition:string,
      drugintervaldosageunitnumb:string,
      drugrecurreadministration:string,
      drugseparatedosagenumb:string,
      drugstartdate:string,
      drugstartdateformat:string,
      drugstructuredosagenumb:string,
      drugstructuredosageunit:string,
      drugtreatmentduration:string,
      drugtreatmentdurationunit:string,
      medicinalproduct:string,
      openfda:struct<
        application_number:array<string>,
        brand_name:array<string>,
        generic_name:array<string>,
        manufacturer_name:array<string>,
        nui:array<string>,
        package_ndc:array<string>,
        pharm_class_cs:array<string>,
        pharm_class_epc:array<string>,
        pharm_class_moa:string,
        pharm_class_pe:string,
        product_ndc:array<string>,
        product_type:array<string>,
        route:array<string>,
        rxcui:array<string>,
        spl_id:array<string>,
        spl_set_id:array<string>,
        substance_name:array<string>,
        unii:array<string>
      >
    >>,
    patientagegroup:string,
    patientonsetage:string,
    patientonsetageunit:string,
    patientsex:string,
    patientweight:string,
    reaction:array<struct<
      reactionmeddrapt:string,
      reactionmeddraversionpt:string,
      reactionoutcome:string
    >>,
    summary:struct<narrativeincludeclinical:string>>,
  primarysource	struct<literaturereference:string,qualification:string,reportercountry:string>,
  primarysourcecountry	string,
  receiptdate	string,
  receiptdateformat	string,
  receivedate	string,
  receivedateformat	string,
  receiver	struct<receiverorganization:string,receivertype:string>,
  reportduplicate	string,
  reporttype	string,
  safetyreportid	string,
  safetyreportversion	string,
  sender	struct<senderorganization:string,sendertype:string>,
  serious	string,
  seriousnesscongenitalanomali	string,
  seriousnessdeath	string,
  seriousnessdisabling	string,
  seriousnesshospitalization	string,
  seriousnesslifethreatening	string,
  seriousnessother	string,
  transmissiondate	string,
  transmissiondateformat	string
  )
USING JSON
OPTIONS (
  path "abfss://openfda@opemfda.dfs.core.windows.net/"
)

-- COMMAND ----------

DROP TABLE IF EXISTS openfda.openfdasilver.drugevent;
CREATE TABLE IF NOT EXISTS openfda.openfdasilver.drugevent
AS
SELECT  concat(safetyreportid, safetyreportversion) as report_id,
  authoritynumb,
  companynumb,
  duplicate,
  fulfillexpeditecriteria,
  occurcountry, 
  primarysource.literaturereference as ps_lit_ref,
  primarysource.qualification as ps_qual,
  primarysource.reportercountry as ps_rpt_country,
  primarysourcecountry,
  receiptdate,
  receiptdateformat,
  receivedate,
  receivedateformat,
  receiver.receiverorganization as rcvr_org,
  receiver.receivertype as rcvr_type,
  reportduplicate,
  reporttype,
  sender.senderorganization as sender_org,
  sender.sendertype as sender_type,
  serious,
  seriousnesscongenitalanomali,
  seriousnessdeath,
  seriousnessdisabling,
  seriousnesshospitalization,
  seriousnesslifethreatening,
  seriousnessother,
  transmissiondate,
  transmissiondateformat
FROM openfda.openfdaraw.drugevent_raw;


-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql.functions import explode,monotonically_increasing_id
-- MAGIC df = spark.sql("SELECT concat(safetyreportid, safetyreportversion) as report_id, patient FROM openfda.openfdaraw.drugevent_raw")
-- MAGIC df1 = df.withColumn("drug", explode("patient.drug")).withColumn("drug_id",monotonically_increasing_id()).withColumn("reaction", explode("patient.reaction")).withColumn("reaction_id",monotonically_increasing_id())

-- COMMAND ----------


DROP TABLE IF EXISTS openfda.openfdasilver.drugevent_patient;
CREATE TABLE IF NOT EXISTS openfda.openfdasilver.drugevent_patient
AS
SELECT  concat(safetyreportid, safetyreportversion) as report_id,
    patient.patientagegroup, 
    patient.patientonsetage, 
    patient.patientonsetageunit,
    patient.patientsex,
    patient.patientweight   
FROM openfda.openfdaraw.drugevent_raw;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC df_drug = df1.select("report_id","drug_id","drug").withColumns({"drug_id":df1.drug_id,"actiondrug":df1.drug.actiondrug,"activesubstancename":df1.drug.activesubstance.activesubstancename,"drugadditional":df1.drug.drugadditional,"drugadministrationroute":df1.drug.drugadministrationroute,"drugauthorizationnumb":df1.drug.drugauthorizationnumb,"drugbatchnumb":df1.drug.drugbatchnumb,"drugcharacterization":df1.drug.drugcharacterization,"drugcumulativedosagenumb":df1.drug.drugcumulativedosagenumb,"drugcumulativedosageunit":df1.drug.drugcumulativedosageunit,"drugdosageform":df1.drug.drugdosageform,"drugdosagetext":df1.drug.drugdosagetext,"drugenddate":df1.drug.drugenddate,"drugenddateformat":df1.drug.drugenddateformat,"drugindication":df1.drug.drugindication,"drugintervaldosagedefinition":df1.drug.drugintervaldosagedefinition,"drugintervaldosageunitnumb":df1.drug.drugintervaldosageunitnumb,"drugrecurreadministration":df1.drug.drugrecurreadministration,"drugseparatedosagenumb":df1.drug.drugseparatedosagenumb,"drugstartdate":df1.drug.drugstartdate,"drugstartdateformat":df1.drug.drugstartdateformat,"drugstructuredosagenumb":df1.drug.drugstructuredosagenumb,"drugstructuredosageunit":df1.drug.drugstructuredosageunit,"drugtreatmentduration":df1.drug.drugtreatmentduration,                         "drugtreatmentdurationunit":df1.drug.drugtreatmentdurationunit,"medicinalproduct":df1.drug.medicinalproduct,}).drop("drug").dropDuplicates()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC df_reaction = df1.select("report_id","reaction_id","reaction").withColumns({
-- MAGIC     "reactionmeddrapt":df1.reaction.reactionmeddrapt,
-- MAGIC     "reactionmeddraversionpt":df1.reaction.reactionmeddraversionpt,
-- MAGIC     "reactionoutcome":df1.reaction.reactionoutcome}).drop("reaction").dropDuplicates()

-- COMMAND ----------

DROP TABLE IF EXISTS openfda.openfdasilver.drugevent_drug;
DROP TABLE IF EXISTS openfda.openfdasilver.drugevent_reaction;
DROP TABLE IF EXISTS openfda.openfdasilver.drugevent_drug_ofda;


-- COMMAND ----------

-- MAGIC %python
-- MAGIC df_drug_ofda = df1.select("report_id","drug_id","drug").withColumns({"nui":df1.drug.openfda.nui,"pharm_class_cs":df1.drug.openfda.pharm_class_cs,"pharm_class_epc":df1.drug.openfda.pharm_class_epc,"pharm_class_moa":df1.drug.openfda.pharm_class_moa,"pharm_class_pe":df1.drug.openfda.pharm_class_pe,"product_type":df1.drug.openfda.product_type[0],"route0":df1.drug.openfda.route[0],"route":df1.drug.openfda.route[1],"substance_name":df1.drug.openfda.substance_name,"unii":df1.drug.openfda.unii })

-- COMMAND ----------

-- MAGIC %python
-- MAGIC df_drug.write.saveAsTable("openfda.openfdasilver.drugevent_drug")
-- MAGIC df_reaction.write.saveAsTable("openfda.openfdasilver.drugevent_reaction")
-- MAGIC df_drug_ofda.write.saveAsTable("openfda.openfdasilver.drugevent_drug_ofda")

-- COMMAND ----------

-- MAGIC
-- MAGIC %python
-- MAGIC from pyspark.sql.functions import explode,monotonically_increasing_id
-- MAGIC df = spark.sql("SELECT distinct UNII FROM openfda.openfdasilver.drugevent_drug_ofda")
-- MAGIC df1 = df.withColumn("UNII", explode("UNII"))

-- COMMAND ----------

-- MAGIC %python
-- MAGIC df1.write.saveAsTable("openfda.openfdasilver.drugevent_unii")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_drug ded ON de.report_id = ded.report_id
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_reaction der ON de.report_id = der.report_id
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_patient dep ON de.report_id = dep.report_id
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_drug_ofda dedo ON de.report_id = dedo.report_id

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql.functions import concat_ws
-- MAGIC
-- MAGIC df = spark.sql("""
-- MAGIC     SELECT *
-- MAGIC     FROM 
-- MAGIC         openfda.openfdasilver.drugevent_patient
-- MAGIC """)
-- MAGIC
-- MAGIC output_path = "abfss://openfda@opemfda.dfs.core.windows.net/drugevent_patient.csv"
-- MAGIC df.write.csv(output_path, header=True)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Gold Tables

-- COMMAND ----------

CREATE SCHEMA openfdagold;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC ####################################################This task was implemented in the Azure SQL #################################
-- MAGIC
-- MAGIC # Use the appropriate catalog and schema
-- MAGIC spark.sql("USE CATALOG openfda")
-- MAGIC spark.sql("USE SCHEMA openfdagold")
-- MAGIC
-- MAGIC # Drop the table if it exists
-- MAGIC spark.sql("DROP TABLE IF EXISTS openfda.openfdagold.drugevent")
-- MAGIC
-- MAGIC # Create the table using the SQL query
-- MAGIC df = spark.sql("""
-- MAGIC SELECT 
-- MAGIC de.report_id,
-- MAGIC concat("This report was produced on ", to_date(de.receivedate)) AS report_date,
-- MAGIC concat(
-- MAGIC   CASE WHEN dep.patientagegroup = 1 THEN "Patient was a neonatal"
-- MAGIC        WHEN dep.patientagegroup = 2 THEN "Patient was a newborn"
-- MAGIC        WHEN dep.patientagegroup = 3 THEN "Patient was an infant"
-- MAGIC        WHEN dep.patientagegroup = 4 THEN "Patient was a child"
-- MAGIC        WHEN dep.patientagegroup = 5 THEN "Patient was an adolescent"
-- MAGIC        WHEN dep.patientagegroup = 6 THEN "Patient was an Adult"
-- MAGIC        WHEN dep.patientagegroup = 7 THEN "Patient was an Elderly"
-- MAGIC        ELSE " "
-- MAGIC        END,
-- MAGIC   CASE WHEN dep.patientsex = 1 THEN 'MALE'
-- MAGIC        WHEN dep.patientsex = 2 THEN 'FEMALE'
-- MAGIC        WHEN dep.patientsex = 3 THEN 'UNKNOWN GENDER'
-- MAGIC        ELSE ""
-- MAGIC        END, 
-- MAGIC   CASE WHEN dep.patientonsetageunit = 800 THEN concat("age ", dep.patientonsetage * 10, " years.")
-- MAGIC        WHEN dep.patientonsetageunit = 801 THEN concat("age ", dep.patientonsetage, " years.")
-- MAGIC        WHEN dep.patientonsetageunit = 802 THEN concat("age ", dep.patientonsetage, " months.")
-- MAGIC        WHEN dep.patientonsetageunit = 803 THEN concat("age ", dep.patientonsetage, " weeks.")  
-- MAGIC        WHEN dep.patientonsetageunit = 804 THEN concat("age ", dep.patientonsetage * 10, " days.")
-- MAGIC        WHEN dep.patientonsetageunit = 805 THEN concat("age ", dep.patientonsetage * 10, " hours.")
-- MAGIC        ELSE " "
-- MAGIC        END
-- MAGIC ) AS P1,
-- MAGIC concat("Patient weight in Kilograms was ", dep.patientweight) AS P2,
-- MAGIC concat("The patient was given a drug whose valid trade name or the generic name is ", ded.medicinalproduct) AS S1,
-- MAGIC concat("The start date of drug administration is ", to_date(ded.drugstartdate)) AS S2,
-- MAGIC concat("The patient stopped taking the drug on ", to_date(ded.drugstartdate)) AS S3,
-- MAGIC concat("The active substance in the drug is ", ded.activesubstancename) AS S4,
-- MAGIC concat("Additional detail about the dosage taken or schedule of administration is ", ded.drugdosagetext) AS S5,
-- MAGIC concat("Indication for the drug’s use says ", ded.drugindication) AS S6, 
-- MAGIC concat("And the patient was given ", ded.drugseparatedosagenumb, " number of separate doses.") AS S7,
-- MAGIC concat("The patient started showing the reaction ", der.reactionmeddrapt) AS S8,
-- MAGIC concat("A total dose of ", drugcumulativedosagenumb, 
-- MAGIC   CASE WHEN ded.drugcumulativedosageunit = "001" THEN " kilograms"
-- MAGIC        WHEN ded.drugcumulativedosageunit = "002" THEN " grams"
-- MAGIC        WHEN ded.drugcumulativedosageunit = "003" THEN " milligrams"
-- MAGIC        WHEN ded.drugcumulativedosageunit = "004" THEN " micrograms"
-- MAGIC        ELSE ""
-- MAGIC        END, " was administered to the patient until the first reaction was experienced."
-- MAGIC ) AS S9,
-- MAGIC concat(
-- MAGIC   CASE WHEN ded.actiondrug = 1 THEN "After the reactions, Drug was withdrawn "
-- MAGIC        WHEN ded.actiondrug = 2 THEN "After the reactions, Dose was reduced "
-- MAGIC        WHEN ded.actiondrug = 3 THEN "After the reactions, Dose was increased "
-- MAGIC        WHEN ded.actiondrug = 4 THEN "After the reactions, Drug was not changed "
-- MAGIC        ELSE "" END, 
-- MAGIC   CASE WHEN ded.drugadditional = 1 THEN "and the reactions abated."
-- MAGIC        WHEN ded.drugadditional = 2 THEN "and the reactions did not abate."
-- MAGIC        ELSE "." END 
-- MAGIC ) AS S10,
-- MAGIC CASE WHEN ded.drugcharacterization = 1 THEN "Suspect - the drug was considered to be the cause of the reactions"
-- MAGIC      WHEN ded.drugcharacterization = 2 THEN "Concomitant - the drug was reported as being taken along with the suspect drug"
-- MAGIC      WHEN ded.drugcharacterization = 3 THEN "Interacting - the drug was considered by the reporter to have interacted with the suspect drug"
-- MAGIC      ELSE ""
-- MAGIC      END AS S11,
-- MAGIC CASE WHEN der.reactionoutcome = 1 THEN "Patient recovered from the reaction or reaction resolved at the time of filing this report"
-- MAGIC      WHEN der.reactionoutcome = 2 THEN "Patient recovering from the reaction or reaction resolving at the time of filing this report"
-- MAGIC      WHEN der.reactionoutcome = 3 THEN "Patient did not recover from the reaction or reaction did not resolve at the time of filing this report"
-- MAGIC      WHEN der.reactionoutcome = 4 THEN "Patient recovered/resolved with sequelae (consequent health issues) at the time of filing this report" 
-- MAGIC      WHEN der.reactionoutcome = 5 THEN "Patient died from the reaction or reaction"
-- MAGIC      ELSE ""
-- MAGIC      END AS S12,
-- MAGIC concat("The substance name of the drug is ", concat_ws(", ", dedo.substance_name)) AS S13,
-- MAGIC concat("The UNII of the drug is ", concat_ws(", ", dedo.unii)) AS S14,
-- MAGIC CASE WHEN de.serious = 1 THEN "The adverse event resulted in death, a life threatening condition, hospitalization, disability, congenital anomaly, or other serious condition"
-- MAGIC      WHEN de.serious = 2 THEN "The adverse event did not result in death, a life threatening condition, hospitalization, disability, congenital anomaly, or other serious condition"
-- MAGIC      ELSE "" END AS S15,
-- MAGIC CASE WHEN de.seriousnesscongenitalanomali = 1 THEN "The adverse event resulted in serious congenital anomaly"
-- MAGIC      ELSE "" END AS S16, 
-- MAGIC CASE WHEN de.seriousnessdeath = 1 THEN "The adverse event resulted in death"
-- MAGIC      ELSE "" END AS S17, 
-- MAGIC CASE WHEN de.seriousnessdisabling = 1 THEN "The adverse event resulted in disability"
-- MAGIC      ELSE "" END AS S18,
-- MAGIC CASE WHEN de.seriousnesshospitalization = 1 THEN "The adverse event resulted in hospitalization"
-- MAGIC      ELSE "" END AS S19,
-- MAGIC CASE WHEN de.seriousnesslifethreatening = 1 THEN "The adverse event resulted in life threatening condition"
-- MAGIC      ELSE "" END AS S20,
-- MAGIC CASE WHEN de.seriousnessother = 1 THEN "The adverse event resulted in other serious conditions"
-- MAGIC      ELSE "" END AS S21
-- MAGIC FROM openfda.openfdasilver.drugevent de
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_drug ded ON de.report_id = ded.report_id
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_reaction der ON de.report_id = der.report_id
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_patient dep ON de.report_id = dep.report_id
-- MAGIC INNER JOIN openfda.openfdasilver.drugevent_drug_ofda dedo ON de.report_id = dedo.report_id
-- MAGIC """)
-- MAGIC
-- MAGIC # Display the dataframe
-- MAGIC display(df)
