-- comotion@172.25.73.200

-- just basic information about each user
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	card_id VARCHAR(50) NOT NULL UNIQUE,
	uw_id INT NOT NULL UNIQUE,
	uw_netid VARCHAR(50) NOT NULL UNIQUE,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL
);

-- keeps track of which card readers users cards will work on
CREATE TABLE memberships (
	id SERIAL PRIMARY KEY,
	uw_id INT NOT NULL REFERENCES users(uw_id),
	type VARCHAR(50) NOT NULL REFERENCES equipment_groups(type),
	join_date INT NOT NULL,
	expiration_date INT
);

-- keeps track of added bans added for users and which card reader type it applies to
CREATE TABLE card_ban (
	id SERIAL PRIMARY KEY,
	uw_id INT NOT NULL REFERENCES users(uw_id),
	type VARCHAR(50) NOT NULL REFERENCES equipment_groups(type),
	start_date INT NOT NULL,
	end_date INT NOT NULL
);

-- keeps track of card swipes when they happen and on which card reader
CREATE TABLE card_activity (
	id SERIAL PRIMARY KEY,
	uw_id INT NOT NULL,
	type VARCHAR(50) NOT NULL REFERENCES equipment_groups(type),
	date INT NOT NULL,
	pass BIT(1) NOT NULL DEFAULT '0'
);

-- keeps track of each card reader by id and its type	
CREATE TABLE card_readers (
	id SERIAL PRIMARY KEY,
	type VARCHAR(50) NOT NULL REFERENCES equipment_groups(type),
	description VARCHAR(200) NOT NULL,
	active BIT(1) NOT NULL DEFAULT '1'
);

-- keeps track of equipment groups for giving user permissions
CREATE TABLE equipment_groups (
	id SERIAL PRIMARY KEY,
	type VARCHAR(50) NOT NULL UNIQUE,
	description VARCHAR(200) NOT NULL,
	active BIT(1) NOT NULL DEFAULT '1'
);

INSERT INTO equipment_groups (type, description) VALUES
	('main_door', 'Main Door'),
	('laser_cutter', 'Laser Cutter'),
	('3d_printer', '3D Printer'),
	('othermill', 'Othermill'),
	('vinyl_cutter', 'Vinyl Cutter');

INSERT INTO card_readers (type, description) VALUES
	('main_door', 'Main Door'),
	('laser_cutter', '60 W Yellow Laser Cutter'),
	('laser_cutter', '150 W Red Laser Cutter'),
	('3d_printer', '3D Printer'),
	('othermill', 'Othermill v2'),
	('othermill', 'Othermill v2'),
	('othermill', 'Othermill Pro'),
	('vinyl_cutter', 'Vinyl Cutter');

INSERT INTO users (card_id, uw_id, uw_netid, first_name, last_name) VALUES
	(16808635, 16808635, 'xsdray', 'Shida', 'Xu'),
	(16808469, 16808469, 'chunter6', 'CHRISTOPHER J.', 'HUNTER'),
	(16808086, 16808086, 'anasilv', 'Ana', 'Silvera'),
	(16808028, 16808028, 'aaraj', 'AARA', 'GOLPAD'),
	(16807551, 16807551, 'clk1391', 'CHARLES LAWSON', 'KELLY'),
	(16807378, 16807378, 'astroc', 'Clarice C.', 'Astronimo'),
	(16807352, 16807352, 'lemcwhor', 'LAUREN E', 'MCWHORTER'),
	(16807223, 16807223, 'noej', 'JESSICA ANN WHITE', 'NOE'),
	(16807215, 16807215, 'corylock', 'CORY MICHAEL', 'LOCK'),
	(16804306, 16804306, 'kieferd', 'KIEFER DOUGLAS', 'DUNDAS'),
	(16801741, 16801741, 'madridg', 'GABRIELA', 'MADRID VALERO'),
	(16798239, 16798239, 'zccope', 'ZANE C.', 'COPE'),
	(16798161, 16798161, 'lml1913', 'LOUIS MICHAEL', 'LOPEZ'),
	(16797981, 16797981, 'haidangt', 'HaiDang T', 'Tran'),
	(16797732, 16797732, 'jamesdr', 'JAMES D', 'ROSENTHAL'),
	(16797553, 16797553, 'gracel54', 'GRACE YOUNG', 'LEE'),
	(16797180, 16797180, 'kyshi', 'KAIYU', 'SHI'),
	(16797122, 16797122, 'zrob', 'ZACHARY', 'ROBBINS'),
	(16796760, 16796760, 'annaml', 'Anna', 'Mlasowsky'),
	(16796607, 16796607, 'nlogler', 'NICHOLAS T', 'LOGLER'),
	(16795915, 16795915, 'randy97n', 'RANDY HIEN', 'NGUYEN'),
	(16795683, 16795683, 'rimas428', 'Samir Bishara', 'Kharoufeh'),
	(16795645, 16795645, 'sando7', 'SEVERIANO ANGELO', 'SANDOMIRSKY'),
	(16795639, 16795639, 'alexb428', 'ALEX RICHARD', 'BERNARD'),
	(16795629, 16795629, 'janeej', 'Janee Lee', 'Johnson'),
	(16795524, 16795524, 'bbgaston', 'BENJAMIN BUI', 'GASTON'),
	(16795407, 16795407, 'smitlb', 'LAURA BEHLKE', 'SMIT'),
	(16795400, 16795400, 'vclarke', 'VICTORIA ANNE', 'CLARKE'),
	(16795393, 16795393, 'kshatos', 'KEAGAN PAUL', 'SHATOS');

INSERT INTO memberships (uw_id, type, join_date, expiration_date) VALUES
	(16808635, 'main_door', 1494610320, 1494610380),
	(16808469, 'laser_cutter', 1494608100, 1494608100),
	(16808086, 'laser_cutter', 1494604200, 1494604200),
	(16808028, 'othermill', 1494603540, 1494603540),
	(16807551, '3d_printer', 1494598800, 1494598800),
	(16807378, 'main_door', 1494597180, 1494597180),
	(16807352, '3d_printer', 1494596940, 1494596940),
	(16807223, 'othermill', 1494595860, 1494595860),
	(16807215, '3d_printer', 1494595800, 1494595800),
	(16804306, '3d_printer', 1494533940, 1494533940),
	(16801741, 'main_door', 1494505380, 1494505380),
	(16798239, 'vinyl_cutter', 1494447780, 1494447780),
	(16798161, 'laser_cutter', 1494446820, 1494446880),
	(16797981, '3d_printer', 1494443880, 1494443880),
	(16797732, '3d_printer', 1494440940, 1494440940),
	(16797553, 'main_door', 1494439680, 1494439680),
	(16797180, 'main_door', 1494436260, 1494436320),
	(16797122, 'laser_cutter', 1494435780, 1494435780),
	(16796760, 'othermill', 1494432900, 1494432900),
	(16796607, 'main_door', 1494431940, 1494431940),
	(16795915, 'main_door', 1494427500, 1494427500),
	(16795683, 'laser_cutter', 1494426180, 1494426180),
	(16795645, '3d_printer', 1494426000, 1494426000),
	(16795639, 'main_door', 1494425940, 1494425940),
	(16795629, 'main_door', 1494425880, 1494425880),
	(16795524, 'laser_cutter', 1494425220, 1494425220),
	(16795407, 'laser_cutter', 1494424260, 1494424260),
	(16795400, 'main_door', 1494424200, 1494424200),
	(16795393, 'main_door', 1494424200, 1494424200),
	(16796760, 'othermill', 1494432900, 1505081737);