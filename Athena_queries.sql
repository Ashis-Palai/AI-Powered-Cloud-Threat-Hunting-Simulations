CREATE EXTERNAL TABLE threat_hunting_db.cloudtrail_logs (
  eventversion STRING,
  eventtime STRING,
  eventsource STRING,
  eventname STRING,
  awsregion STRING,
  sourceipaddress STRING,
  useragent STRING,
  eventtype STRING,
  eventcategory STRING,
  apiversion STRING,
  managementevent BOOLEAN,
  readonly BOOLEAN,
  recipientaccountid STRING,
  sessioncredentialfromconsole BOOLEAN,

  useridentity STRUCT<
    type: STRING,
    principalid: STRING,
    arn: STRING,
    accountid: STRING,
    accesskeyid: STRING,
    sessioncontext: STRUCT<
      sessionissuer: STRUCT<
        type: STRING,
        principalid: STRING,
        arn: STRING,
        accountid: STRING,
        username: STRING
      >,
      attributes: STRUCT<
        creationdate: STRING,
        mfaauthenticated: STRING
      >
    >
  >,

  requestparameters STRING,
  responseelements STRING,
  additionaleventdata STRING,
  serviceeventdetails STRING,
  tlsdetails STRING,

  requestid STRING,
  eventid STRING
)
PARTITIONED BY (
  year STRING,
  month STRING,
  day STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'true'
)
LOCATION 's3://threat-hunting-lake/cloudtrail/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.year.type' = 'integer',
  'projection.year.range' = '2020,2030',
  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',
  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',
  'storage.location.template' =
  's3://threat-hunting-lake/cloudtrail/year=${year}/month=${month}/day=${day}/'
);

*****************************************************************************

SELECT
  eventtime,
  eventsource,
  eventname,
  sourceipaddress,
  awsregion,
  requestparameters,
  useridentity.type AS identity_type,
  useridentity.arn AS identity_arn
FROM threat_hunting_db.cloudtrail_logs
WHERE year = '2025'
  AND month = '12'
  AND day = '14'
LIMIT 3;
**************************************

CREATE EXTERNAL TABLE threat_hunting_db.guardduty_findings (
  accountid                     STRING,
  arn                           STRING,
  id                            STRING,
  region                        STRING,
  schemaversion                 STRING,
  severity                      DOUBLE,
  confidence                    DOUBLE,
  type                          STRING,
  partition                     STRING,
  title                         STRING,
  description                   STRING,
  createdat                     STRING,
  updatedat                     STRING,
  associatedattacksequencearn   STRING,
  resource STRUCT<
    resourcetype: STRING
  >,
  service STRUCT<
    servicename: STRING,
    featurename: STRING,
    detectorid: STRING,
    archived: BOOLEAN,
    count: INT,
    eventfirstseen: STRING,
    eventlastseen: STRING,
    resourcerole: STRING,
    action: STRING,
    detection: STRING,
    runtimedetails: STRING
  >
)
PARTITIONED BY (
  year  STRING,
  month STRING,
  day   STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'true',
  'case.insensitive' = 'true'
)
LOCATION 's3://threat-hunting-lake/guardduty/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.year.type'  = 'integer',
  'projection.year.range' = '2020,2030',
  'projection.month.type'   = 'integer',
  'projection.month.range'  = '1,12',
  'projection.month.digits' = '2',
  'projection.day.type'   = 'integer',
  'projection.day.range'  = '1,31',
  'projection.day.digits' = '2',
  'storage.location.template' =
    's3://threat-hunting-lake/guardduty/year=${year}/month=${month}/day=${day}/'
);
*****************************
SELECT *
FROM threat_hunting_db.guardduty_findings
WHERE year = '2025'
  AND month = '12'
  AND day = '14'
LIMIT 3;
********************

CREATE EXTERNAL TABLE threat_hunting_db.vpc_flow_logs (
  version INT,
  account_id STRING,
  interface_id STRING,
  instance_id STRING,
  vpc_id STRING,
  subnet_id STRING,
  region STRING,
  az_id STRING,

  srcaddr STRING,
  dstaddr STRING,
  srcport INT,
  dstport INT,
  protocol INT,

  packets BIGINT,
  bytes BIGINT,

  start BIGINT,
  end_time BIGINT,

  action STRING,
  log_status STRING,

  flow_direction STRING,
  type STRING,
  tcp_flags INT,
  traffic_path INT
)
PARTITIONED BY (
  year STRING,
  month STRING,
  day STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'true',
  'case.insensitive' = 'true'
)
LOCATION 's3://threat-hunting-lake/vpc_flowlog/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.year.type' = 'integer',
  'projection.year.range' = '2020,2030',
  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',
  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',
  'storage.location.template' =
  's3://threat-hunting-lake/vpc_flowlog/year=${year}/month=${month}/day=${day}/'
);
*******************************
CREATE EXTERNAL TABLE threat_hunting_db.waf_logs (
  action STRING,
  clientip STRING,
  country STRING,
  formatversion INT,
  httpmethod STRING,
  httpsourceid STRING,
  httpsourcename STRING,
  timestamp BIGINT,
  uri STRING,
  args STRING,
  webaclid STRING,
  httpversion STRING,
  requestid STRING,

  headers STRING,
  ja3fingerprint STRING,
  labels ARRAY<STRING>,
  nonterminatingmatchingrules STRING,

  terminatingruleid STRING,
  terminatingruletype STRING
)
PARTITIONED BY (
  year STRING,
  month STRING,
  day STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'true',
  'case.insensitive' = 'true'
)
LOCATION 's3://threat-hunting-lake/web_acl_waf_logs/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.year.type' = 'integer',
  'projection.year.range' = '2020,2030',
  'projection.month.type' = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',
  'projection.day.type' = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',
  'storage.location.template' =
  's3://threat-hunting-lake/web_acl_waf_logs/year=${year}/month=${month}/day=${day}/'
);
*************************************
SELECT from_unixtime(timestamp / 1000) AS event_time, clientip, country, httpmethod, uri, args, action, headers, labels, terminatingruleid, terminatingruletype
FROM threat_hunting_db.waf_logs
WHERE year = '2025' AND month = '12' AND day = '14'
  AND httpmethod IN ('POST','PUT')
  AND (uri LIKE '%upload%' OR uri LIKE '%file%' OR uri LIKE '%attachment%' OR uri LIKE '%.php%' OR uri LIKE '%.jsp%' OR uri LIKE '%.asp%' OR uri LIKE '%.aspx%' OR uri LIKE '%.war%')
  AND (args LIKE '%file%' OR args LIKE '%upload%' OR args LIKE '%name=%' OR args LIKE '%.php%' OR args LIKE '%.jsp%' OR args LIKE '%.asp%' OR args LIKE '%.aspx%' OR args LIKE '%.phtml%' OR args LIKE '%.phar%' OR args LIKE '%.war%' OR args LIKE '%.zip%' OR args LIKE '%.tar%' OR args LIKE '%.gz%')
  AND (lower(headers) LIKE '%curl%' OR lower(headers) LIKE '%wget%' OR lower(headers) LIKE '%python%' OR lower(headers) LIKE '%httpclient%')
ORDER BY event_time ASC;
*******************************

SELECT from_iso8601_timestamp(createdat) AS event_time, id AS finding_id, type AS finding_type,
       severity, confidence, title, resource.resourcetype AS resource_type,
       service.featurename AS feature_name, service.eventfirstseen, service.eventlastseen,
       service.runtimedetails
FROM threat_hunting_db.guardduty_findings
WHERE year = '2025' AND month = '12' AND day = '14'
  AND from_iso8601_timestamp(createdat)
      BETWEEN timestamp '2025-12-14 10:30:00' AND timestamp '2025-12-14 11:00:00'
  AND type LIKE '%Runtime%'
ORDER BY event_time ASC;
******************************
