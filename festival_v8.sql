/* DDL ξεκινω να οριζω τις οντοτητες και δε βαζω καθολου κλειδια, μονο τ attributes για αρχη. 
Αυριο θα κανω σε χαρτι το σχημα να δω ποιες σχεσεις περιττευουν και τοτε θα φτιαξω εδω τους 
πινακες των σχεσεων και θα βαλω κλειδια
 */
DROP DATABASE IF EXISTS fest;
DROP DATABASE IF EXISTS Festival;
CREATE DATABASE Festival;
USE Festival;

-- Create Location table 
CREATE TABLE Location (
    ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Latitude DECIMAL(9,6) NOT NULL,
    Longitude DECIMAL(9,6) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Continent VARCHAR(100) NOT NULL,
    UNIQUE (Latitude, Longitude),
    UNIQUE (Address, City, Country, Continent)
);

-- Create Stage table (renamed the second Stage table to Performer_Stage)
CREATE TABLE Stage (
    ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description VARCHAR(255),
    Capacity INT NOT NULL,
    Tech_Info VARCHAR(255) NOT NULL
);

CREATE TABLE Visitor (
    ID INT PRIMARY KEY,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    Age INT,
    Con_Info VARCHAR(255)
);

-- Create Festival table
CREATE TABLE Festival (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    Location_ID INT NOT NULL,
    UNIQUE (Location_ID),
    Year INT GENERATED ALWAYS AS (YEAR(Start_Date)) STORED, -- Generated column for the year
    UNIQUE (Year),  -- Unique constraint on the generated year column
    FOREIGN KEY (Location_ID) REFERENCES Location(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create Event table (Removed PERIOD FOR syntax)
CREATE TABLE Event (
    ID INT PRIMARY KEY,
    Start_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    End_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    Sold_Out BOOLEAN NOT NULL,
    Festival_ID INT NOT NULL,
    Stage_ID INT NOT NULL,
    UNIQUE (Festival_ID, Stage_ID, Start_Time),
    FOREIGN KEY (Festival_ID) REFERENCES Festival(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Stage_ID) REFERENCES Stage(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Resale_Queue (
    ID INT PRIMARY KEY,
    Activated BOOLEAN,
    Activation_Date DATE,
    Event_ID INT,
    UNIQUE (Event_ID),
    FOREIGN KEY (Event_ID) REFERENCES Event(ID)
);

CREATE TABLE Buy_Queue (
    ID INT PRIMARY KEY,
    Type_ID VARCHAR(100),
    Event_ID INT,
    Timestamp DATETIME,
    FOREIGN KEY (Event_ID) REFERENCES Event(ID)
);

-- Create Performer table
CREATE TABLE Performer (
    ID INT PRIMARY KEY,
    Real_Name VARCHAR(100),
    Stage_Name VARCHAR(100) NOT NULL,
    Birthday DATE,
    Instagram VARCHAR(100),
    Website VARCHAR(100),
    Is_Band BOOLEAN NOT NULL,
    Formation_Date DATE
);

CREATE TABLE Performance (
    ID INT PRIMARY KEY,
    Type VARCHAR(100) NOT NULL CHECK (Type IN ('Warm up', 'Head line', 'Special guest')),
    Start_Time TIME NOT NULL,
    Duration INT NOT NULL CHECK (Duration > 0 AND Duration <= 180),
    Performer_ID INT NOT NULL,
    Event_ID INT NOT NULL,
    UNIQUE (Event_ID, Performer_ID),
    FOREIGN KEY (Performer_ID) REFERENCES Performer(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Event_ID) REFERENCES Event(ID) ON DELETE CASCADE ON UPDATE CASCADE
);


-- Create Staff table
CREATE TABLE Staff (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Age INT NOT NULL CHECK (Age > 0),
    Type VARCHAR(100) NOT NULL CHECK (Type IN ('Trainee', 'Beginner', 'Intermediate', 'Experienced', 'Very Experienced'))
);

CREATE TABLE Support_Staff (
    Staff_ID INT PRIMARY KEY,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Security_Staff (
    Staff_ID INT PRIMARY KEY,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Technical_Staff (
    Staff_ID INT PRIMARY KEY,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Membership table: Artist is member of Band
CREATE TABLE Membership (
    Band_ID INT NOT NULL,
    Artist_ID INT NOT NULL,
    Join_Date DATE,
    PRIMARY KEY (Band_ID, Artist_ID),
    FOREIGN KEY (Band_ID) REFERENCES Performer(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Artist_ID) REFERENCES Performer(ID) ON DELETE CASCADE ON UPDATE CASCADE
);


-- Create Genre table 
CREATE TABLE Genre (
    ID INT PRIMARY KEY,
    Name VARCHAR(100)
);


-- Optional: Subgenre table
CREATE TABLE Subgenre (
    ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Genre_ID INT NOT NULL,
    FOREIGN KEY (Genre_ID) REFERENCES Genre(ID) ON DELETE CASCADE ON UPDATE CASCADE
);


-- Optional: Performer's Subgenres (many-to-many)
CREATE TABLE Performer_Subgenre (
    Performer_ID INT NOT NULL,
    Subgenre_ID INT NOT NULL,
    PRIMARY KEY (Performer_ID, Subgenre_ID),
    FOREIGN KEY (Performer_ID) REFERENCES Performer(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Subgenre_ID) REFERENCES Subgenre(ID) ON DELETE CASCADE ON UPDATE CASCADE
);


-- Create event_staff table 
-- (Event is not null even though there is not full participation of staff in the relation.
--  This happens because unemployed staff members are not mentioned in any tupple participating in the relationship,
--  due to on delete cascade constraint. So in order to detect unemployed staff members we simply search for them in 
--  the relationship table.)
CREATE TABLE event_staff (
    Staff_ID INT NOT NULL,
    Event_ID INT NOT NULL,
    PRIMARY KEY (Staff_ID, Event_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Event_ID) REFERENCES Event(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Type (
    Name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Payment (
    Name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Ticket (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    EAN_CODE VARCHAR(200),
    Stage_Info VARCHAR(300),
    Price DECIMAL(10,2),
    Activated BOOLEAN DEFAULT FALSE,
    Date_Bought DATE,
    Type_ID VARCHAR(100),
    Payment_ID VARCHAR(100),
    Event_ID INT,
    UNIQUE (EAN_CODE),
    FOREIGN KEY (Type_ID) REFERENCES Type(Name),
    FOREIGN KEY (Payment_ID) REFERENCES Payment(Name),
    FOREIGN KEY (Event_ID) REFERENCES Event(ID)
);

CREATE TABLE Tickets_In_Resale (
    Ticket_ID INT PRIMARY KEY,
    Resale_Queue_ID INT,
    FOREIGN KEY (Ticket_ID) REFERENCES Ticket(ID),
    FOREIGN KEY (Resale_Queue_ID) REFERENCES Resale_Queue(ID)
);

CREATE TABLE Spectator (
    Visitor_ID INT,
    Ticket_ID INT,
    PRIMARY KEY (Visitor_ID, Ticket_ID),
    FOREIGN KEY (Visitor_ID) REFERENCES Visitor(ID),
    FOREIGN KEY (Ticket_ID) REFERENCES Ticket(ID)
);

CREATE TABLE Visitor_Interested_Event (
    Event_ID INT NOT NULL,
    Visitor_ID INT NOT NULL,
    Type_ID VARCHAR(100) NOT NULL,
    PRIMARY KEY (Event_ID, Visitor_ID, Type_ID),
    FOREIGN KEY (Event_ID) REFERENCES Event(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Visitor_ID) REFERENCES Visitor(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Type_ID) REFERENCES Type(Name) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Visitor_Waitlisted (
    Buy_Queue_ID INT,
    Visitor_ID INT,
    PRIMARY KEY (Buy_Queue_ID, Visitor_ID),
    FOREIGN KEY (Buy_Queue_ID) REFERENCES Buy_Queue(ID),
    FOREIGN KEY (Visitor_ID) REFERENCES Visitor(ID)
);

CREATE TABLE Transaction (
    ID INT PRIMARY KEY,
    Is_Resale BOOLEAN,
    Ticket_ID INT,
    Buyer_ID INT,
    UNIQUE (Ticket_ID, Buyer_ID),
    FOREIGN KEY (Ticket_ID) REFERENCES Ticket(ID),
    FOREIGN KEY (Buyer_ID) REFERENCES Visitor(ID)
);

CREATE TABLE Visitor_Sold_Ticket (
    Seller_ID INT,
    Ticket_ID INT,
    Transaction_ID INT,
    PRIMARY KEY (Seller_ID, Ticket_ID),
    FOREIGN KEY (Seller_ID) REFERENCES Visitor(ID),
    FOREIGN KEY (Ticket_ID) REFERENCES Ticket(ID),
    FOREIGN KEY (Transaction_ID) REFERENCES Transaction(ID)
);

CREATE TABLE Review (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Interpretation INT,
    Sound INT,
    Lighting INT,
    Stage_Presence INT,
    Organization INT,
    Overall INT,
    Ticket_ID INT,
    UNIQUE (Ticket_ID),
    FOREIGN KEY (Ticket_ID) REFERENCES Ticket(ID)
);

--images
CREATE TABLE Image (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    URL VARCHAR(255),
    Description VARCHAR(255)
) 

CREATE TABLE Festival_Image (
    Festival_ID INT,
    Image_ID INT,
    PRIMARY KEY (Festival_ID, Image_ID),
    FOREIGN KEY (Festival_ID) REFERENCES Festival(ID) ON UPDATE CASCADE,
    FOREIGN KEY (Image_ID) REFERENCES Image(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Performer_Image (
    Performer_ID INT,
    Image_ID INT,
    PRIMARY KEY (Performer_ID, Image_ID),
    FOREIGN KEY (Performer_ID) REFERENCES Performer(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Image_ID) REFERENCES Image(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Stage_Image (
    Stage_ID INT,
    Image_ID INT,
    PRIMARY KEY (Stage_ID, Image_ID),
    FOREIGN KEY (Stage_ID) REFERENCES Stage(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Image_ID) REFERENCES Image(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Staff_Image (
    Staff_ID INT,
    Image_ID INT,
    PRIMARY KEY (Staff_ID, Image_ID),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Image_ID) REFERENCES Image(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Event_Image (
    Event_ID INT,
    Image_ID INT,
    PRIMARY KEY (Event_ID, Image_ID),
    FOREIGN KEY (Event_ID) REFERENCES Event(ID) ON UPDATE CASCADE,
    FOREIGN KEY (Image_ID) REFERENCES Image(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Location_Image (
    Location_ID INT,
    Image_ID INT,
    PRIMARY KEY (Location_ID, Image_ID),
    FOREIGN KEY (Location_ID) REFERENCES Location(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Image_ID) REFERENCES Image(ID) ON DELETE CASCADE ON UPDATE CASCADE
);

-------------------------------------------------------------------------------------------------------------------
---------------------   T R I G G E R S ---------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------

-- Create trigger: FESTIVAL CANNOT BE CANCELDED
DELIMITER $$

CREATE TRIGGER prevent_festival_deletion
BEFORE DELETE ON Festival
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Festival deletion is not allowed.';
END$$

DELIMITER ;


-- Create trigger: EVENT CANNOT BE CANCELLED
DELIMITER $$

CREATE TRIGGER prevent_event_deletion
BEFORE DELETE ON Event
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Event deletion is not allowed.';
END$$

DELIMITER ;


-- Create trigger: BAND CANNOT BE MEMBER OF BAND
DELIMITER $$

CREATE TRIGGER prevent_band_as_member
BEFORE INSERT ON Membership
FOR EACH ROW
BEGIN
    DECLARE is_band_member BOOLEAN;

    -- Check if the performer being added as a member is a band
    SELECT Is_Band INTO is_band_member
    FROM Performer
    WHERE ID = NEW.Artist_ID;

    -- If the member is a band, prevent the insertion
    IF is_band_member = TRUE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A band cannot be a member of another band.';
    END IF;
END$$

DELIMITER ;


-- Create trigger for INTERVALS (from 5 to 30 mins) 
-- between consecutive performances of the same event
DELIMITER $$
CREATE TRIGGER check_performance_break
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
  DECLARE last_end TIME;
  DECLARE diff INT;

  -- get the last performance’s end-time on this event
  SELECT ADDTIME(Start_Time,
                 SEC_TO_TIME(Duration * 60))
    INTO last_end
    FROM Performance
    WHERE Event_ID = NEW.Event_ID
    ORDER BY Start_Time DESC
    LIMIT 1;

  IF last_end IS NOT NULL THEN
    SET diff = TIMESTAMPDIFF(MINUTE,
                             last_end,
                             NEW.Start_Time);
    IF diff < 5 OR diff > 30 THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
          'There must be a break between 5 and 30 minutes.';
    END IF;
  END IF;
END$$
DELIMITER ;


-- Create trigger: NO OVERLAP OF EVENTS AT THE SAME STAGE
DELIMITER $$

CREATE TRIGGER prevent_stage_overlap
BEFORE INSERT ON Event
FOR EACH ROW
BEGIN
    DECLARE overlap_found INT;

    -- Check for overlap
    SELECT COUNT(*)
    INTO overlap_found
    FROM Event p
    WHERE p.Stage_ID = NEW.Stage_ID
      AND (
           (NEW.Start_Time BETWEEN p.Start_Time AND p.End_Time)
        OR (NEW.End_Time BETWEEN p.Start_Time AND p.End_Time)
        OR (p.Start_Time BETWEEN NEW.Start_Time AND NEW.End_Time)
        OR (p.End_Time BETWEEN NEW.Start_Time AND NEW.End_Time)
      );

    -- If overlap is found, signal an error
    IF overlap_found > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stage already occupied during this time.';
    END IF;
END $$

DELIMITER;


-- Create trigger: NO DOUBLE BOOKING OF PERFORMERS
DELIMITER $$

CREATE TRIGGER prevent_overlapping_performances
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
    DECLARE new_start TIME;
    DECLARE new_end TIME;

    SET new_start = NEW.Start_Time;
    SET new_end = ADDTIME(NEW.Start_Time, SEC_TO_TIME(NEW.Duration * 60));

    -- 1. Same performer overlap check
    IF EXISTS (
        SELECT 1
        FROM Performance p
        WHERE p.Performer_ID = NEW.Performer_ID
          AND p.Event_ID != NEW.Event_ID
          AND (
                (new_start BETWEEN p.Start_Time AND ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)))
             OR (new_end BETWEEN p.Start_Time AND ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)))
             OR (p.Start_Time BETWEEN new_start AND new_end)
             OR (ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)) BETWEEN new_start AND new_end)
          )
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Performer is already in a performance during this time.';
    END IF;

    -- 2. Artist’s bands overlap
    IF EXISTS (
        SELECT 1
        FROM Membership m
        JOIN Performance p ON p.Performer_ID = m.Band_ID
        WHERE m.Artist_ID = NEW.Performer_ID
          AND (
                (new_start BETWEEN p.Start_Time AND ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)))
             OR (new_end BETWEEN p.Start_Time AND ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)))
             OR (p.Start_Time BETWEEN new_start AND new_end)
             OR (ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)) BETWEEN new_start AND new_end)
          )
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'One of the performer’s bands is already performing during this time.';
    END IF;

    -- 3. Band member overlap
    IF EXISTS (
        SELECT 1
        FROM Membership m
        JOIN Performance p ON p.Performer_ID = m.Artist_ID
        WHERE m.Band_ID = NEW.Performer_ID
          AND (
                (new_start BETWEEN p.Start_Time AND ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)))
             OR (new_end BETWEEN p.Start_Time AND ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)))
             OR (p.Start_Time BETWEEN new_start AND new_end)
             OR (ADDTIME(p.Start_Time, SEC_TO_TIME(p.Duration * 60)) BETWEEN new_start AND new_end)
          )
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A member of the band is already performing during this time.';
    END IF;
END $$

DELIMITER ;


-- Create trigger: AFTER DELETION OF PERFRORMANCE
DELIMITER $$

CREATE TRIGGER after_performance_delete
AFTER DELETE ON Performance
FOR EACH ROW
BEGIN
    -- Call the procedure to reschedule performances in the same event
    CALL Reschedule_Performances_After_Deletion(OLD.Event_ID);
END$$

DELIMITER ;


-- Create trigger: ARTIST CANNOT PRTICIPATE FOR FOUR CONSECUTIVE YEARS
DELIMITER $$

CREATE TRIGGER prevent_fourth_consecutive_year
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
    DECLARE perf_year INT;
    DECLARE consecutive_count INT;

    -- 1) Find the year of the FESTIVAL to which this new performance belongs
    SELECT YEAR(f.Start_Date)
      INTO perf_year
      FROM Event e
      JOIN Festival f ON e.Festival_ID = f.ID
     WHERE e.ID = NEW.Event_ID;

    -- 2) Count how many distinct years in the 3 immediately preceding years
    SELECT COUNT(DISTINCT YEAR(f2.Start_Date))
      INTO consecutive_count
      FROM Performance p
      JOIN Event e2 ON p.Event_ID = e2.ID
      JOIN Festival f2 ON e2.Festival_ID = f2.ID
     WHERE p.Performer_ID = NEW.Performer_ID
       AND YEAR(f2.Start_Date) BETWEEN perf_year - 3 AND perf_year - 1;

    -- 3) If already in all of the last 3 years, block the 4th
    IF consecutive_count = 3 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ο performer δεν μπορεί να συμμετέχει για 4η συνεχόμενη χρονιά.';
    END IF;
END$$

DELIMITER ;


 
-- Έλεγχος μέγιστης χωρητικότητας σκηνής κατά την πώληση εισιτηρίου
DELIMITER $$

CREATE TRIGGER prevent_ticket_overbooking
BEFORE INSERT ON Spectator
FOR EACH ROW
BEGIN
    DECLARE max_capacity INT;
    DECLARE current_tickets INT;

    -- Πάρε χωρητικότητα σκηνής
    SELECT s.Capacity INTO max_capacity
    FROM Ticket t
    JOIN Event e ON t.Event_ID = e.ID
    JOIN Stage s ON e.Stage_ID = s.ID
    WHERE t.ID = NEW.Ticket_ID;

    -- Υπολόγισε εισιτήρια που έχουν πουληθεί
    SELECT COUNT(*) INTO current_tickets
    FROM Spectator sp
    JOIN Ticket t ON sp.Ticket_ID = t.ID
    WHERE t.Event_ID = (
        SELECT Event_ID FROM Ticket WHERE ID = NEW.Ticket_ID
    );

    IF current_tickets >= max_capacity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stage capacity reached – ticket cannot be sold.';
    END IF;
END$$

DELIMITER ;


-- Ένα εισιτήριο ανά παράσταση/ημέρα/επισκέπτη
DELIMITER $$

CREATE TRIGGER prevent_duplicate_ticket_purchase
BEFORE INSERT ON Spectator
FOR EACH ROW
BEGIN
    DECLARE cnt INT;
    DECLARE ticket_event_id INT;
    DECLARE ticket_date DATE;

    -- Πάρε ημερομηνία και event
    SELECT Event_ID, Date_Bought INTO ticket_event_id, ticket_date
    FROM Ticket WHERE ID = NEW.Ticket_ID;

    SELECT COUNT(*) INTO cnt
    FROM Spectator sp
    JOIN Ticket t ON sp.Ticket_ID = t.ID
    WHERE sp.Visitor_ID = NEW.Visitor_ID
      AND t.Event_ID = ticket_event_id;

    IF cnt > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Visitor already has a ticket for this event.';
    END IF;
END$$

DELIMITER ;


-- Έλεγχος VIP εισιτηρίων ≤ 10% της χωρητικότητας σκηνής
DELIMITER $$

CREATE TRIGGER limit_vip_tickets
BEFORE INSERT ON Ticket
FOR EACH ROW
BEGIN
    DECLARE vip_limit INT;
    DECLARE current_vip INT;
    DECLARE capacity INT;

    -- Πάρε χωρητικότητα σκηνής
    SELECT s.Capacity INTO capacity
    FROM Stage s
    JOIN Event e ON e.Stage_ID = s.ID
    WHERE e.ID = NEW.Event_ID;

    SET vip_limit = CEIL(capacity * 0.10);

    -- Υπολόγισε VIP εισιτήρια για το event
    SELECT COUNT(*) INTO current_vip
    FROM Ticket
    WHERE Event_ID = NEW.Event_ID AND Type_ID = 'VIP';

    IF NEW.Type_ID = 'VIP' AND current_vip >= vip_limit THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'VIP ticket limit reached for this stage.';
    END IF;
END$$

DELIMITER ;

-- Επιβεβαίωση ενεργοποίησης εισιτηρίου κατά την είσοδο
DELIMITER $$

CREATE TRIGGER prevent_double_activation
BEFORE UPDATE ON Ticket
FOR EACH ROW
BEGIN
    IF OLD.Activated = TRUE AND NEW.Activated = TRUE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ticket is already activated.';
    END IF;
END$$

DELIMITER ;


-- TRIGGER: REVIEWS ONLY BY ACTIVATED TICKETS
DELIMITER $$

CREATE TRIGGER trg_check_valid_review
BEFORE INSERT ON Review
FOR EACH ROW
BEGIN
    DECLARE v_Activated BOOLEAN;
    DECLARE v_Match INT;

    SELECT Activated INTO v_Activated
    FROM Ticket
    WHERE ID = NEW.Ticket_ID;

    IF v_Activated = FALSE THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Το εισιτήριο δεν έχει ενεργοποιηθεί. Δεν μπορείτε να υποβάλετε αξιολόγηση.';
    END IF;

    SELECT COUNT(*) INTO v_Match
    FROM Spectator
    WHERE Ticket_ID = NEW.Ticket_ID;

    IF v_Match = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Δεν είστε κάτοχος αυτού του εισιτηρίου.';
    END IF;
END$$

DELIMITER;


-- Trigger: BEFORE INSERT ON Visitor_Interested_Event CHECK IF EVENT SOLD OUT
DELIMITER $$

CREATE TRIGGER trg_before_insert_vie
BEFORE INSERT ON Visitor_Interested_Event
FOR EACH ROW
BEGIN
    CALL handle_visitor_interest(NEW.Visitor_ID, NEW.Event_ID, NEW.Type_ID);
END$$

DELIMITER ;


-- Trigger: BEFORE INSERT ON BUY QUEUE CHECK TICKETS IN RESALE 
DELIMITER $$

CREATE TRIGGER trg_before_buy_queue
AFTER INSERT ON Buy_Queue
FOR EACH ROW
BEGIN
    DECLARE v_Has_Tickets BOOLEAN;
    DECLARE v_Ticket_ID INT;

    -- Check if there are resale tickets for the event and category
    SELECT COUNT(*) > 0 INTO v_Has_Tickets
    FROM Tickets_In_Resale TIR
    JOIN Ticket T ON T.ID = TIR.Ticket_ID
    WHERE T.Event_ID = NEW.Event_ID AND T.Type_ID = NEW.Type_ID;

    -- If resale ticket exists, assign it and prevent queue insert
    IF v_Has_Tickets THEN

        -- Get a ticket to assign
        SELECT TIR.Ticket_ID INTO v_Ticket_ID
        FROM Tickets_In_Resale TIR
        JOIN Ticket T ON T.ID = TIR.Ticket_ID
        WHERE T.Event_ID = NEW.Event_ID AND T.Type_ID = NEW.Type_ID
        LIMIT 1;

        -- Reassign spectator to new visitor (buyer)
        UPDATE Spectator
        SET Visitor_ID = NEW.Visitor_ID
        WHERE Ticket_ID = v_Ticket_ID;

        -- Create resale transaction
        INSERT INTO Transaction (ID, Is_Resale, Ticket_ID, Buyer_ID)
        VALUES (UUID_SHORT(), TRUE, v_Ticket_ID, NEW.Visitor_ID);

        -- Remove ticket from resale pool
        DELETE FROM Tickets_In_Resale WHERE Ticket_ID = v_Ticket_ID;

        -- Prevent insert into Buy_Queue
        DELETE FROM Buy_Queue
        WHERE ID = NEW.ID;

    END IF;

END$$

DELIMITER ;

-- Trigger: BEFORE INSERT ON RESALE QUEUE CHECK BUY QUEUE
DELIMITER $$

CREATE TRIGGER trg_before_insert_resale_queue
BEFORE INSERT ON Resale_Queue
FOR EACH ROW
BEGIN
    DECLARE v_Ticket_ID INT;
    DECLARE v_Category VARCHAR(100);
    DECLARE v_Visitor_ID INT;
    DECLARE v_Buy_Queue_ID INT;

    -- Step 1: Find the ticket to be resold (assumes passed via NEW.Ticket_ID)
    SELECT Type_ID INTO v_Type_ID
    FROM Ticket
    WHERE ID = NEW.Ticket_ID;

    -- Step 2: Find the first visitor in Buy_Queue for this event and category
    SELECT BQ.ID, VWE.Visitor_ID INTO v_Buy_Queue_ID, v_Visitor_ID
    FROM Buy_Queue BQ
    JOIN Visitor_Waitlisted VWE ON VWE.Buy_Queue_ID = BQ.ID
    WHERE BQ.Event_ID = NEW.Event_ID AND BQ.Type_ID = v_Type_ID
    ORDER BY BQ.Timestamp ASC
    LIMIT 1;

    -- Step 3: If such visitor exists, reassign ticket
    IF v_Visitor_ID IS NOT NULL THEN

        -- Update Spectator to reassign ticket
        UPDATE Spectator
        SET Visitor_ID = v_Visitor_ID
        WHERE Ticket_ID = NEW.Ticket_ID;

        -- Insert resale transaction
        INSERT INTO Transaction (ID, Is_Resale, Ticket_ID, Buyer_ID)
        VALUES (UUID_SHORT(), TRUE, NEW.Ticket_ID, v_Visitor_ID);

        -- Remove visitor from waitlist and queue
        DELETE FROM Visitor_Waitlisted
        WHERE Buy_Queue_ID = v_Buy_Queue_ID AND Visitor_ID = v_Visitor_ID;

        DELETE FROM Buy_Queue WHERE ID = v_Buy_Queue_ID;

    ELSE
        -- Step 4: No matching buyer, insert into Tickets_In_Resale
        INSERT INTO Tickets_In_Resale (Ticket_ID, Resale_Queue_ID)
        VALUES (NEW.Ticket_ID, NEW.ID);
    END IF;

END$$

DELIMITER ;


-- Trigger: BEFORE INSERT ON TRANSACTION UPDATE SPECTATOR
DELIMITER $$

CREATE TRIGGER trg_update_spectator_before_transaction
BEFORE INSERT ON Transaction
FOR EACH ROW
BEGIN

    IF NEW.Is_Resale = TRUE THEN
        -- Remove old spectator record
        DELETE FROM Spectator WHERE Ticket_ID = NEW.Ticket_ID;

        -- Add new spectator
        INSERT INTO Spectator (Visitor_ID, Ticket_ID)
        VALUES (NEW.Buyer_ID, NEW.Ticket_ID);
    END IF;

END$$

DELIMITER ;


------------------------------------------------------------------------------------------------------------------
--------------  P R O C E D U R E S ------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------

-- Create procedure: HANDLE DELETION OF PERFORMANCE
DELIMITER $$

CREATE PROCEDURE Reschedule_Performances_After_Deletion(IN deleted_event_id INT)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE perf_id INT;
    DECLARE perf_type VARCHAR(100);
    DECLARE perf_duration INT;
    DECLARE perf_performer INT;

    DECLARE current_start TIME;
    DECLARE cur CURSOR FOR
        SELECT ID, Type, Duration, Performer_ID
        FROM Performance
        WHERE Event_ID = deleted_event_id
        ORDER BY Start_Time ASC;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Step 1: Delete all performances for this event
    DELETE FROM Performance WHERE Event_ID = deleted_event_id;

    -- Step 2: Get event start time
    SELECT Start_Time INTO current_start
    FROM Event WHERE ID = deleted_event_id;

    -- Step 3: Re-insert performances with 5 min gaps
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO perf_id, perf_type, perf_duration, perf_performer;
        IF done THEN
            LEAVE read_loop;
        END IF;

        INSERT INTO Performance (ID, Type, Start_Time, Duration, Performer_ID, Event_ID)
        VALUES (
            perf_id, perf_type, current_start, perf_duration, perf_performer, deleted_event_id
        );

        -- Update start time for next performance: current + duration + 5 mins
        SET current_start = ADDTIME(current_start, SEC_TO_TIME(perf_duration * 60 + 5 * 60));
    END LOOP;

    CLOSE cur;
END$$

DELIMITER ;


-- Create procedure that validates staff coverage and autoassigns more staff
DELIMITER //

CREATE PROCEDURE AutoAssignStaff(IN p_Event_ID INT)
BEGIN
    DECLARE v_TotalSpectators INT DEFAULT 0;
    DECLARE v_RequiredSecurity INT DEFAULT 0;
    DECLARE v_RequiredSupport INT DEFAULT 0;
    DECLARE v_CurrentSecurity INT DEFAULT 0;
    DECLARE v_CurrentSupport INT DEFAULT 0;

    -- Get number of spectators
    SELECT COUNT(*) INTO v_TotalSpectators
    FROM Spectator S
    JOIN Ticket T ON S.Ticket_ID = T.ID
    WHERE T.Event_ID = p_Event_ID;

    -- Calculate required staff
    SET v_RequiredSecurity = CEIL(0.05 * v_TotalSpectators);
    SET v_RequiredSupport = CEIL(0.02 * v_TotalSpectators);

    -- Get current counts
    SELECT COUNT(*) INTO v_CurrentSecurity
    FROM event_staff es
    JOIN Security_Staff ss ON es.Staff_ID = ss.Staff_ID
    WHERE es.Event_ID = p_Event_ID;

    SELECT COUNT(*) INTO v_CurrentSupport
    FROM event_staff es
    JOIN Support_Staff ss ON es.Staff_ID = ss.Staff_ID
    WHERE es.Event_ID = p_Event_ID;

    -- Assign additional security staff if needed
    WHILE v_CurrentSecurity < v_RequiredSecurity DO
        INSERT INTO event_staff (Staff_ID, Event_ID)
        SELECT ss.Staff_ID, p_Event_ID
        FROM Security_Staff ss
        WHERE ss.Staff_ID NOT IN (
            SELECT Staff_ID FROM event_staff WHERE Event_ID = p_Event_ID
        )
        LIMIT 1;

        SET v_CurrentSecurity = v_CurrentSecurity + 1;
    END WHILE;

    -- Assign additional support staff if needed
    WHILE v_CurrentSupport < v_RequiredSupport DO
        INSERT INTO event_staff (Staff_ID, Event_ID)
        SELECT ss.Staff_ID, p_Event_ID
        FROM Support_Staff ss
        WHERE ss.Staff_ID NOT IN (
            SELECT Staff_ID FROM event_staff WHERE Event_ID = p_Event_ID
        )
        LIMIT 1;

        SET v_CurrentSupport = v_CurrentSupport + 1;
    END WHILE;
END;
//

DELIMITER ;


--Procedure to scan ticket

DELIMITER $$
 
CREATE PROCEDURE ScanTicket(IN p_Ticket_ID INT)
BEGIN
    DECLARE v_Activated BOOLEAN;

    SELECT Activated INTO v_Activated
    FROM Ticket
    WHERE ID = p_Ticket_ID;
 
    IF v_Activated THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Το εισιτήριο έχει ήδη ενεργοποιηθεί.';
    ELSE
        UPDATE Ticket
        SET Activated = TRUE
        WHERE ID = p_Ticket_ID;
    END IF;
 
END$$
 
DELIMITER ;
 

-- Procedure: CHECK EVENT SOLD OUT (TICKETS SOLD <= STAGE CAPACITY)
DELIMITER $$

CREATE PROCEDURE is_event_sold_out(IN p_Event_ID INT, OUT p_Is_Sold_Out BOOLEAN)
BEGIN
    DECLARE v_Capacity INT;
    DECLARE v_Tickets_Sold INT;

    SELECT S.Capacity INTO v_Capacity
    FROM Event E
    JOIN Stage S ON E.Stage_ID = S.ID
    WHERE E.ID = p_Event_ID;

    SELECT COUNT(*) INTO v_Tickets_Sold
    FROM Ticket T
    JOIN Spectator SP ON SP.Ticket_ID = T.ID
    WHERE T.Event_ID = p_Event_ID;

    SET p_Is_Sold_Out = (v_Tickets_Sold >= v_Capacity);
END$$

DELIMITER ;

-- Procedure: IF EVENT SOLD OUY ACTIVATE RESALE QUEUE
DELIMITER $$

CREATE PROCEDURE activate_resale_if_sold_out(IN p_Event_ID INT)
BEGIN
    DECLARE v_Is_Sold_Out BOOLEAN;

    CALL is_event_sold_out(p_Event_ID, v_Is_Sold_Out);

    IF v_Is_Sold_Out THEN
        UPDATE Resale_Queue
        SET Activated = TRUE, Activation_Date = CURDATE()
        WHERE Event_ID = p_Event_ID;
    END IF;
END$$

DELIMITER ;


-- Procedure: HANDLE VISITOR INTERESTED IN EVENT (SPECTATOR OR WAITLISTED)
DELIMITER $$

CREATE PROCEDURE handle_visitor_interest(IN p_Visitor_ID INT, IN p_Event_ID INT, IN p_Type_ID INT)
BEGIN
    DECLARE v_Is_Sold_Out BOOLEAN;
    DECLARE v_New_Ticket_ID INT;

    -- Check if the event is sold out
    CALL is_event_sold_out(p_Event_ID, v_Is_Sold_Out);

    IF v_Is_Sold_Out THEN
        -- Event is sold out → put visitor in buy queue and waitlist
        INSERT INTO Buy_Queue (Type_ID, Event_ID, Timestamp)
        VALUES (p_Type_ID, p_Event_ID, NOW());

        INSERT INTO Visitor_Waitlisted (Visitor_ID, Buy_Queue_ID)
        VALUES (p_Visitor_ID, LAST_INSERT_ID());

    ELSE
        -- Event is not sold out → assign ticket and add as spectator
        INSERT INTO Ticket (Type_ID, Event_ID, Activated)
        VALUES (p_Type_ID, p_Event_ID, FALSE);

        SET v_New_Ticket_ID = LAST_INSERT_ID();

        INSERT INTO Spectator (Visitor_ID, Ticket_ID)
        VALUES (p_Visitor_ID, v_New_Ticket_ID);

        INSERT INTO Transaction (Is_Resale, Ticket_ID, Buyer_ID)
        VALUES (FALSE, v_New_Ticket_ID, p_Visitor_ID)

    END IF;
END$$

DELIMITER ;
 

-- PROCEDURE: AFTER TRANSACTION REGISTER BUYER AND SELLER (IF EXISTS) 


-- Procedure: PUT IN RESALE
DELIMITER $$

CREATE PROCEDURE resell_unused_ticket(IN p_Ticket_ID INT)
BEGIN
    DECLARE v_Event_ID INT;
    DECLARE v_Queue_ID INT;
    DECLARE v_Activated BOOLEAN;

    -- Ensure ticket is not activated
    SELECT Activated INTO v_Activated
    FROM Ticket
    WHERE ID = p_Ticket_ID;

    IF v_Activated THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ticket already activated and cannot be resold.';
    END IF;

    -- Find Event ID
    SELECT Event_ID INTO v_Event_ID
    FROM Ticket
    WHERE ID = p_Ticket_ID;

    -- Find corresponding resale queue
    SELECT ID INTO v_Queue_ID
    FROM Resale_Queue
    WHERE Event_ID = v_Event_ID AND Activated = TRUE;

    -- Insert ticket into resale
    INSERT INTO Tickets_In_Resale (Ticket_ID, Resale_Queue_ID)
    VALUES (p_Ticket_ID, v_Queue_ID);
END$$

DELIMITER ;
  

-- PROCEDURE: PROCESS RESALE QUEUE 
DELIMITER $$
 
CREATE PROCEDURE Process_Resale_Queue(IN p_Event_ID INT)

BEGIN

    DECLARE v_Ticket_ID INT;
    DECLARE v_Buyer_ID INT;
    DECLARE v_Category VARCHAR(100);
    DECLARE v_Queue_ID INT;
    DECLARE v_Buy_Queue_ID INT;
    DECLARE done BOOLEAN DEFAULT FALSE;
 
    -- Cursor για διαθέσιμα εισιτήρια προς μεταπώληση
    DECLARE ticket_cursor CURSOR FOR

        SELECT TIR.Ticket_ID
        FROM Tickets_In_Resale TIR
        JOIN Ticket T ON T.ID = TIR.Ticket_ID
        WHERE T.Event_ID = p_Event_ID;
 
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    OPEN ticket_cursor;
 
    read_loop: LOOP
        FETCH ticket_cursor INTO v_Ticket_ID;
        IF done THEN
            LEAVE read_loop;
        END IF;
 
        -- Πάρε κατηγορία εισιτηρίου
        SELECT Type_ID INTO v_Category
        FROM Ticket
        WHERE ID = v_Ticket_ID;
 

        -- Βρες τον πρώτο αγοραστή (Visitor_ID + Buy_Queue_ID) με subquery
        SELECT sub.Visitor_ID, sub.Buy_Queue_ID INTO v_Buyer_ID, v_Buy_Queue_ID 
        FROM (
            SELECT VWE.Visitor_ID, BQ.ID AS Buy_Queue_ID
            FROM Visitor_Waitlisted VWE
            JOIN Buy_Queue BQ ON VWE.Buy_Queue_ID = BQ.ID
            WHERE BQ.Event_ID = p_Event_ID AND BQ.Ticket_Category = v_Category
            ORDER BY BQ.Timestamp ASC
            LIMIT 1
        ) AS sub;
 

        -- Αν υπάρχει αγοραστής, προχώρα σε μεταπώληση
        IF v_Buyer_ID IS NOT NULL THEN

            -- Διαγραφή προηγούμενου κατόχου
            DELETE FROM Spectator
            WHERE Ticket_ID = v_Ticket_ID;
 

            -- Προσθήκη νέου κατόχου
            INSERT INTO Spectator (Visitor_ID, Ticket_ID)
            VALUES (v_Buyer_ID, v_Ticket_ID);

            -- Καταγραφή της συναλλαγής
            INSERT INTO Transaction (ID, Is_Resale, Ticket_ID, Buyer_ID)
            VALUES (UUID_SHORT(), TRUE, v_Ticket_ID, v_Buyer_ID);
 
            -- Αφαίρεση από Tickets_In_Resale
            DELETE FROM Tickets_In_Resale
            WHERE Ticket_ID = v_Ticket_ID;

            -- Αφαίρεση από Visitor_Waitlisted
            DELETE FROM Visitor_Waitlisted
            WHERE Buy_Queue_ID = v_Buy_Queue_ID AND Visitor_ID = v_Buyer_ID;

            -- Αφαίρεση από Buy_Queue
            DELETE FROM Buy_Queue
            WHERE ID = v_Buy_Queue_ID;
 
        END IF;

    END LOOP;
    CLOSE ticket_cursor;

END$$
 
DELIMITER ;


------------------------------------------------------------------------------------------------------------------
--------------  V I E W S ----------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------

-- Συμμετοχές Καλλιτεχνών ανά Έτος
CREATE VIEW View_Artist_Participation_Per_Year AS
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    YEAR(f.Start_Date) AS Year,
    COUNT(DISTINCT e.ID) AS Total_Events
FROM Performer pe
JOIN Performance p ON pe.ID = p.Performer_ID
JOIN Event e ON p.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
GROUP BY pe.ID, YEAR(f.Start_Date);

-- Έσοδα ανά Έτος και Τρόπο Πληρωμής
CREATE VIEW View_Revenue_Per_Year AS
SELECT 
    YEAR(t.Date_Bought) AS Year,
    pay.Name AS Payment_Method,
    SUM(t.Price) AS Total_Revenue
FROM Ticket t
JOIN Payment pay ON t.Payment_ID = pay.Name
GROUP BY YEAR(t.Date_Bought), pay.Name;

-- Μέσες Αξιολογήσεις ανά Καλλιτέχνη
CREATE VIEW View_Performer_Ratings AS
SELECT 
    pe.ID AS Performer_ID,
    pe.Stage_Name,
    AVG(r.Interpretation) AS Avg_Interpretation,
    AVG(r.Overall) AS Avg_Overall
FROM Performer pe
JOIN Performance p ON pe.ID = p.Performer_ID
JOIN Ticket t ON p.Event_ID = t.Event_ID
JOIN Review r ON r.Ticket_ID = t.ID
GROUP BY pe.ID;

-- Παραστάσεις που παρακολούθησε κάθε επισκέπτης
CREATE VIEW View_Visitor_Attendance AS
SELECT 
    v.ID AS Visitor_ID,
    v.First_Name,
    v.Last_Name,
    e.ID AS Event_ID,
    f.Name AS Festival_Name,
    DATE(f.Start_Date) AS Festival_Date,
    r.Overall AS Visitor_Overall_Score
FROM Visitor v
JOIN Spectator sp ON v.ID = sp.Visitor_ID
JOIN Ticket t ON sp.Ticket_ID = t.ID
JOIN Event e ON t.Event_ID = e.ID
JOIN Festival f ON e.Festival_ID = f.ID
LEFT JOIN Review r ON r.Ticket_ID = t.ID;

-- CREATE VIEW View_Staff_Assignment AS
SELECT 
    e.ID AS Event_ID,
    f.Name AS Festival_Name,
    s.ID AS Staff_ID,
    s.Name AS Staff_Name,
    CASE 
        WHEN ss.Staff_ID IS NOT NULL THEN 'Security'
        WHEN ts.Staff_ID IS NOT NULL THEN 'Technical'
        WHEN su.Staff_ID IS NOT NULL THEN 'Support'
        ELSE 'Unknown'
    END AS Staff_Category
FROM Event e
JOIN Festival f ON e.Festival_ID = f.ID
JOIN event_staff es ON e.ID = es.Event_ID
JOIN Staff s ON es.Staff_ID = s.ID
LEFT JOIN Security_Staff ss ON ss.Staff_ID = s.ID
LEFT JOIN Technical_Staff ts ON ts.Staff_ID = s.ID
LEFT JOIN Support_Staff su ON su.Staff_ID = s.ID;
