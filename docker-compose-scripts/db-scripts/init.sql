CREATE TABLE provider
(
	id smallint NOT NULL PRIMARY KEY,
	name varchar(20) NOT NULL
);

CREATE TABLE type
(
	id smallint PRIMARY KEY NOT NULL,
	name varchar(10) NOT NULL
);

CREATE TABLE access_type
(
	id smallint PRIMARY KEY NOT NULL,
	name varchar(15) NOT NULL
);

CREATE TABLE isp
(
	id int PRIMARY KEY NOT NULL,
	name varchar(150)
);

CREATE TABLE continent
(
	code char(2) PRIMARY KEY NOT NULL,
	name varchar(20) NOT NULL
);

CREATE TABLE country
(
	code char(2) PRIMARY KEY NOT NULL,
	name varchar(50) NOT NULL,
	continent_code char(2) NOT NULL REFERENCES continent(code)
);

CREATE TABLE city
(
	proxy_address varchar(15) PRIMARY KEY NOT NULL,
	latitude decimal,
	longitude decimal,
	name varchar(100),
	sub_division1 varchar(100),
	sub_division1_code varchar(3),
	sub_division2 varchar(100),
	sub_division2_code varchar(3),
	postal_code varchar(20),
	accuracy_radius smallint,
	timezone varchar(50)
);

CREATE TABLE proxy
(
	id SERIAL PRIMARY KEY NOT NULL,
	address varchar(15) NOT NULL REFERENCES city(proxy_address),
	port int NOT NULL,
	country_code char(2) REFERENCES country(code),
	type_id smallint REFERENCES type(id) NOT NULL,
	access_type_id smallint REFERENCES access_type(id) NOT NULL,
	provider_id smallint REFERENCES provider(id) NOT NULL,
	isp_id int REFERENCES isp(id),
	speed int NOT NULL,
	uptime smallint NOT NULL,
	created_date timestamp NOT NULL,
	modified_date timestamp NOT NULL
);

CREATE UNIQUE INDEX proxy_address_port_ui ON proxy (address, port, type_id);
ALTER TABLE proxy
ADD CONSTRAINT proxy_address_port_uc UNIQUE USING INDEX proxy_address_port_ui;

INSERT INTO access_type (id, name) VALUES 
(1, 'Transparent'),
(2, 'Anonymous'),
(3, 'Elite');

INSERT INTO type(id, name) VALUES
(1, 'Http'),
(2, 'Https'),
(3, 'Http/s'),
(4, 'Socks4'),
(5, 'Socks5'),
(6, 'Socks4/5');

INSERT INTO provider (id, name) VALUES
(1, 'Pldown'),
(2, 'ProxyScrape');

INSERT INTO continent (code, name) VALUES
('EU', 'Europe'),
('AF', 'Africa'),
('AS', 'Asia'),
('AN', 'Antarctica'),
('OC', 'Oceania'),
('NA', 'North America'),
('SA', 'South America');

INSERT INTO country (code, name, continent_code) VALUES
('AD', 'Andorra' ,'EU'),
('AE', 'United Arab Emirates' ,'AS'),
('AF', 'Afghanistan' ,'AS'),
('AG', 'Antigua and Barbuda' ,'NA'),
('AI', 'Anguilla' ,'NA'),
('AL', 'Albania' ,'EU'),
('AM', 'Armenia' ,'AS'),
('AO', 'Angola' ,'AF'),
('AQ', 'Antarctica' ,'AN'),
('AR', 'Argentina' ,'SA'),
('AS', 'American Samoa' ,'OC'),
('AT', 'Austria' ,'EU'),
('AU', 'Australia' ,'OC'),
('AW', 'Aruba' ,'NA'),
('AX', 'Åland Islands' ,'EU'),
('AZ', 'Azerbaijan' ,'AS'),
('BA', 'Bosnia and Herzegovina' ,'EU'),
('BB', 'Barbados' ,'NA'),
('BD', 'Bangladesh' ,'AS'),
('BE', 'Belgium' ,'EU'),
('BF', 'Burkina Faso' ,'AF'),
('BG', 'Bulgaria' ,'EU'),
('BH', 'Bahrain' ,'AS'),
('BI', 'Burundi' ,'AF'),
('BJ', 'Benin' ,'AF'),
('BL', 'Saint Barthélemy' ,'NA'),
('BM', 'Bermuda' ,'NA'),
('BN', 'Brunei' ,'AS'),
('BO', 'Bolivia' ,'SA'),
('BQ', 'Bonaire, Sint Eustatius, and Saba' ,'NA'),
('BR', 'Brazil' ,'SA'),
('BS', 'Bahamas' ,'NA'),
('BT', 'Bhutan' ,'AS'),
('BV', 'Bouvet Island' ,'AN'),
('BW', 'Botswana' ,'AF'),
('BY', 'Belarus' ,'EU'),
('BZ', 'Belize' ,'NA'),
('CA', 'Canada' ,'NA'),
('CC', 'Cocos (Keeling) Islands' ,'AS'),
('CD', 'DR Congo' ,'AF'),
('CF', 'Central African Republic' ,'AF'),
('CG', 'Congo Republic' ,'AF'),
('CH', 'Switzerland' ,'EU'),
('CI', 'Ivory Coast' ,'AF'),
('CK', 'Cook Islands' ,'OC'),
('CL', 'Chile' ,'SA'),
('CM', 'Cameroon' ,'AF'),
('CN', 'China' ,'AS'),
('CO', 'Colombia' ,'SA'),
('CR', 'Costa Rica' ,'NA'),
('CU', 'Cuba' ,'NA'),
('CV', 'Cabo Verde' ,'AF'),
('CW', 'Curaçao' ,'NA'),
('CX', 'Christmas Island' ,'OC'),
('CY', 'Cyprus' ,'EU'),
('CZ', 'Czechia' ,'EU'),
('DE', 'Germany' ,'EU'),
('DJ', 'Djibouti' ,'AF'),
('DK', 'Denmark' ,'EU'),
('DM', 'Dominica' ,'NA'),
('DO', 'Dominican Republic' ,'NA'),
('DZ', 'Algeria' ,'AF'),
('EC', 'Ecuador' ,'SA'),
('EE', 'Estonia' ,'EU'),
('EG', 'Egypt' ,'AF'),
('EH', 'Western Sahara' ,'AF'),
('ER', 'Eritrea' ,'AF'),
('ES', 'Spain' ,'EU'),
('ET', 'Ethiopia' ,'AF'),
('FI', 'Finland' ,'EU'),
('FJ', 'Fiji' ,'OC'),
('FK', 'Falkland Islands' ,'SA'),
('FM', 'Federated States of Micronesia' ,'OC'),
('FO', 'Faroe Islands' ,'EU'),
('FR', 'France' ,'EU'),
('GA', 'Gabon' ,'AF'),
('GB', 'United Kingdom' ,'EU'),
('GD', 'Grenada' ,'NA'),
('GE', 'Georgia' ,'AS'),
('GF', 'French Guiana' ,'SA'),
('GG', 'Guernsey' ,'EU'),
('GH', 'Ghana' ,'AF'),
('GI', 'Gibraltar' ,'EU'),
('GL', 'Greenland' ,'NA'),
('GM', 'Gambia' ,'AF'),
('GN', 'Guinea' ,'AF'),
('GP', 'Guadeloupe' ,'NA'),
('GQ', 'Equatorial Guinea' ,'AF'),
('GR', 'Greece' ,'EU'),
('GS', 'South Georgia and the South Sandwich Islands' ,'AN'),
('GT', 'Guatemala' ,'NA'),
('GU', 'Guam' ,'OC'),
('GW', 'Guinea - Bissau' ,'AF'),
('GY', 'Guyana' ,'SA'),
('HK', 'Hong Kong' ,'AS'),
('HM', 'Heard Island and McDonald Islands' ,'AN'),
('HN', 'Honduras' ,'NA'),
('HR', 'Croatia' ,'EU'),
('HT', 'Haiti' ,'NA'),
('HU', 'Hungary' ,'EU'),
('ID', 'Indonesia' ,'AS'),
('IE', 'Ireland' ,'EU'),
('IL', 'Israel' ,'AS'),
('IM', 'Isle of Man' ,'EU'),
('IN', 'India' ,'AS'),
('IO', 'British Indian Ocean Territory' ,'AS'),
('IQ', 'Iraq' ,'AS'),
('IR', 'Iran' ,'AS'),
('IS', 'Iceland' ,'EU'),
('IT', 'Italy' ,'EU'),
('JE', 'Jersey' ,'EU'),
('JM', 'Jamaica' ,'NA'),
('JO', 'Hashemite Kingdom of Jordan' ,'AS'),
('JP', 'Japan' ,'AS'),
('KE', 'Kenya' ,'AF'),
('KG', 'Kyrgyzstan' ,'AS'),
('KH', 'Cambodia' ,'AS'),
('KI', 'Kiribati' ,'OC'),
('KM', 'Comoros' ,'AF'),
('KN', 'St Kitts and Nevis' ,'NA'),
('KP', 'North Korea' ,'AS'),
('KR', 'South Korea' ,'AS'),
('KW', 'Kuwait' ,'AS'),
('KY', 'Cayman Islands' ,'NA'),
('KZ', 'Kazakhstan' ,'AS'),
('LA', 'Laos' ,'AS'),
('LB', 'Lebanon' ,'AS'),
('LC', 'Saint Lucia' ,'NA'),
('LI', 'Liechtenstein' ,'EU'),
('LK', 'Sri Lanka' ,'AS'),
('LR', 'Liberia' ,'AF'),
('LS', 'Lesotho' ,'AF'),
('LT', 'Republic of Lithuania' ,'EU'),
('LU', 'Luxembourg' ,'EU'),
('LV', 'Latvia' ,'EU'),
('LY', 'Libya' ,'AF'),
('MA', 'Morocco' ,'AF'),
('MC', 'Monaco' ,'EU'),
('MD', 'Republic of Moldova' ,'EU'),
('ME', 'Montenegro' ,'EU'),
('MF', 'Saint Martin' ,'NA'),
('MG', 'Madagascar' ,'AF'),
('MH', 'Marshall Islands' ,'OC'),
('MK', 'North Macedonia' ,'EU'),
('ML', 'Mali' ,'AF'),
('MM', 'Myanmar' ,'AS'),
('MN', 'Mongolia' ,'AS'),
('MO', 'Macao' ,'AS'),
('MP', 'Northern Mariana Islands' ,'OC'),
('MQ', 'Martinique' ,'NA'),
('MR', 'Mauritania' ,'AF'),
('MS', 'Montserrat' ,'NA'),
('MT', 'Malta' ,'EU'),
('MU', 'Mauritius' ,'AF'),
('MV', 'Maldives' ,'AS'),
('MW', 'Malawi' ,'AF'),
('MX', 'Mexico' ,'NA'),
('MY', 'Malaysia' ,'AS'),
('MZ', 'Mozambique' ,'AF'),
('NA', 'Namibia' ,'AF'),
('NC', 'New Caledonia' ,'OC'),
('NE', 'Niger' ,'AF'),
('NF', 'Norfolk Island' ,'OC'),
('NG', 'Nigeria' ,'AF'),
('NI', 'Nicaragua' ,'NA'),
('NL', 'Netherlands' ,'EU'),
('NO', 'Norway' ,'EU'),
('NP', 'Nepal' ,'AS'),
('NR', 'Nauru' ,'OC'),
('NU', 'Niue' ,'OC'),
('NZ', 'New Zealand' ,'OC'),
('OM', 'Oman' ,'AS'),
('PA', 'Panama' ,'NA'),
('PE', 'Peru' ,'SA'),
('PF', 'French Polynesia' ,'OC'),
('PG', 'Papua New Guinea' ,'OC'),
('PH', 'Philippines' ,'AS'),
('PK', 'Pakistan' ,'AS'),
('PL', 'Poland' ,'EU'),
('PM', 'Saint Pierre and Miquelon' ,'NA'),
('PN', 'Pitcairn Islands' ,'OC'),
('PR', 'Puerto Rico' ,'NA'),
('PS', 'Palestine' ,'AS'),
('PT', 'Portugal' ,'EU'),
('PW', 'Palau' ,'OC'),
('PY', 'Paraguay' ,'SA'),
('QA', 'Qatar' ,'AS'),
('RE', 'Réunion' ,'AF'),
('RO', 'Romania' ,'EU'),
('RS', 'Serbia' ,'EU'),
('RU', 'Russia' ,'EU'),
('RW', 'Rwanda' ,'AF'),
('SA', 'Saudi Arabia' ,'AS'),
('SB', 'Solomon Islands' ,'OC'),
('SC', 'Seychelles' ,'AF'),
('SD', 'Sudan' ,'AF'),
('SE', 'Sweden' ,'EU'),
('SG', 'Singapore' ,'AS'),
('SH', 'Saint Helena' ,'AF'),
('SI', 'Slovenia' ,'EU'),
('SJ', 'Svalbard and Jan Mayen' ,'EU'),
('SK', 'Slovakia' ,'EU'),
('SL', 'Sierra Leone' ,'AF'),
('SM', 'San Marino' ,'EU'),
('SN', 'Senegal' ,'AF'),
('SO', 'Somalia' ,'AF'),
('SR', 'Suriname' ,'SA'),
('SS', 'South Sudan' ,'AF'),
('ST', 'São Tomé and Príncipe' ,'AF'),
('SV', 'El Salvador' ,'NA'),
('SX', 'Sint Maarten' ,'NA'),
('SY', 'Syria' ,'AS'),
('SZ', 'Eswatini' ,'AF'),
('TC', 'Turks and Caicos Islands' ,'NA'),
('TD', 'Chad' ,'AF'),
('TF', 'French Southern Territories' ,'AN'),
('TG', 'Togo' ,'AF'),
('TH', 'Thailand' ,'AS'),
('TJ', 'Tajikistan' ,'AS'),
('TK', 'Tokelau' ,'OC'),
('TL', 'East Timor' ,'OC'),
('TM', 'Turkmenistan' ,'AS'),
('TN', 'Tunisia' ,'AF'),
('TO', 'Tonga' ,'OC'),
('TR', 'Turkey' ,'AS'),
('TT', 'Trinidad and Tobago' ,'NA'),
('TV', 'Tuvalu' ,'OC'),
('TW', 'Taiwan' ,'AS'),
('TZ', 'Tanzania' ,'AF'),
('UA', 'Ukraine' ,'EU'),
('UG', 'Uganda' ,'AF'),
('UM', 'U.S.Minor Outlying Islands' ,'OC'),
('US', 'United States' ,'NA'),
('UY', 'Uruguay' ,'SA'),
('UZ', 'Uzbekistan' ,'AS'),
('VA', 'Vatican City' ,'EU'),
('VC', 'Saint Vincent and the Grenadines' ,'NA'),
('VE', 'Venezuela' ,'SA'),
('VG', 'British Virgin Islands' ,'NA'),
('VI', 'U.S.Virgin Islands' ,'NA'),
('VN', 'Vietnam' ,'AS'),
('VU', 'Vanuatu' ,'OC'),
('WF', 'Wallis and Futuna' ,'OC'),
('WS', 'Samoa' ,'OC'),
('XK', 'Kosovo' ,'EU'),
('YE', 'Yemen' ,'AS'),
('YT', 'Mayotte' ,'AF'),
('ZA', 'South Africa' ,'AF'),
('ZM', 'Zambia' ,'AF'),
('ZW', 'Zimbabwe' ,'AF');

CREATE TYPE udt_isp AS
(
	id int,
	name varchar(150)
);

CREATE TYPE udt_city AS
(
	proxy_address varchar(15),
	latitude decimal,
	longitude decimal,
	name varchar(100),
	sub_division1 varchar(100),
	sub_division1_code varchar(3),
	sub_division2 varchar(100),
	sub_division2_code varchar(3),
	postal_code varchar(20),
	accuracy_radius smallint,
	timezone varchar(50)
);

CREATE TYPE udt_proxy AS
(
	address varchar(15),
	port int,
	country_code char(2),
	type_id smallint,
	access_type_id smallint,
	provider_id smallint,
	isp_id int,
	speed int,
	uptime smallint
);

CREATE TYPE udt_insert_count AS
(
	insert_proxy_count int,
	insert_city_count int,
	insert_isp_count int,
	update_proxy_count int
);

CREATE TYPE udt_cleanup_count AS
(
	proxy_count int,
	city_count int,
	isp_count int
);

CREATE OR REPLACE FUNCTION fn_insert_proxies(isps json, cities json, proxies json)
RETURNS udt_insert_count AS $func$
DECLARE result_count udt_insert_count;
BEGIN
	WITH isp_count AS
    (
        INSERT INTO isp (id, name)
        SELECT * FROM json_populate_recordset(null::udt_isp, isps) as udt_isps
        ON CONFLICT (id)
        DO NOTHING RETURNING xmax
    )
    SELECT COUNT(*) FILTER (WHERE xmax = 0)
    INTO result_count.insert_isp_count
    FROM isp_count;

	WITH city_count AS
    (
        INSERT INTO city (proxy_address, latitude, longitude, name, sub_division1, sub_division1_code, sub_division2, sub_division2_code, postal_code, accuracy_radius, timezone)
        SELECT * FROM json_populate_recordset(null::udt_city, cities)
        ON CONFLICT (proxy_address)
        DO NOTHING RETURNING xmax
    )
    SELECT COUNT(*) FILTER (WHERE xmax = 0)
    INTO result_count.insert_city_count
    FROM city_count;

    WITH proxy_count AS
    (
        INSERT INTO proxy as p (address, port, country_code, type_id, access_type_id, provider_id, isp_id, speed, uptime, created_date, modified_date)
        SELECT *, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP FROM json_populate_recordset(null::udt_proxy, proxies)
        ON CONFLICT ON CONSTRAINT proxy_address_port_uc
        DO UPDATE SET speed = p.speed, uptime = p.uptime, modified_date = CURRENT_TIMESTAMP RETURNING xmax
    )
    SELECT COUNT(*) FILTER (WHERE xmax = 0),
           COUNT(*) FILTER (WHERE xmax::text::int > 0)
    INTO result_count.insert_proxy_count, result_count.update_proxy_count
    FROM proxy_count;

    RETURN result_count;
END
$func$  LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_get_cleanup_proxies(cleanup_range integer)
RETURNS TABLE (id int,
			   address varchar(15),
			   port int,
			   type smallint,
			   country_code char(2)) AS
$func$
BEGIN
	RETURN QUERY
	SELECT p.id, p.address, p.port, p.type_id, p.country_code FROM proxy as p WHERE modified_date < NOW() - INTERVAL '1 hour' * cleanup_range;
END
$func$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_cleanup_proxies(proxies_range_ids int[], working_proxies json)
RETURNS udt_cleanup_count AS $func$
DECLARE result_count udt_cleanup_count;
BEGIN

    WITH input_working_proxies AS (SELECT * FROM json_populate_recordset(null::udt_proxy, working_proxies))
    UPDATE proxy
    SET type_id = iwp.type_id, access_type_id = iwp.access_type_id, speed = iwp.speed, uptime = iwp.uptime, modified_date = CURRENT_TIMESTAMP
    FROM input_working_proxies as iwp
    WHERE proxy.address = iwp.address AND proxy.port = iwp.port AND proxy.type_id = iwp.type_id;

    WITH input_working_proxies AS (SELECT * FROM json_populate_recordset(null::udt_proxy, working_proxies)),
	input_proxy_range AS (SELECT * FROM unnest(proxies_range_ids::int[])),
    stale_proxies AS (SELECT * FROM input_proxy_range EXCEPT (SELECT p.id FROM input_working_proxies as iwp INNER JOIN proxy AS p ON iwp.address = p.address AND iwp.port = p.port AND iwp.type_id = p.type_id)),
    good_proxies AS (SELECT p.id, p.address, p.isp_id FROM proxy as p WHERE p.id NOT IN (SELECT * FROM input_proxy_range)),
    old_proxies_city AS (SELECT address FROM proxy WHERE address NOT IN (SELECT address FROM good_proxies) AND address NOT IN (SELECT address FROM input_working_proxies)),
    old_proxies_isp AS (SELECT isp_id FROM proxy WHERE isp_id NOT IN (SELECT isp_id FROM good_proxies) AND isp_id NOT IN (SELECT isp_id FROM input_working_proxies)),
    deleted_proxy AS (DELETE FROM proxy WHERE id IN (SELECT * FROM stale_proxies) RETURNING *),
    deleted_isp AS (DELETE FROM isp WHERE id IN (SELECT * FROM old_proxies_isp) RETURNING *),
    deleted_city AS (DELETE FROM city WHERE proxy_address IN (SELECT * FROM old_proxies_city) RETURNING *)

    SELECT (SELECT count(*) FROM deleted_proxy), (SELECT count(*) FROM deleted_city), (SELECT count(*) FROM deleted_isp)
    INTO result_count.proxy_count, result_count.city_count, result_count.isp_count;

    RETURN result_count;
END
$func$  LANGUAGE plpgsql;