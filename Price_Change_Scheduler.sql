-- 1) Make sure the scheduler is running
SET GLOBAL event_scheduler = ON;

-- 2) Create (or replace) the daily event
CREATE EVENT IF NOT EXISTS update_ticket_prices_random
ON SCHEDULE
  EVERY 1 DAY
  STARTS '2025-05-09 00:05:00'
COMMENT 'Daily random price adjustment between -1% and +5%'
DO
  UPDATE Ticket t
  JOIN Event e
    ON t.Event_ID = e.ID
  SET
    -- new price = old price * (1 + (RAND()*0.06 - 0.01))
    t.Price = ROUND(
      t.Price * (1 + (RAND() * 0.06 - 0.01))
    , 2)
  WHERE
    -- only adjust tickets for events still in the future
    e.Start_Date > CURDATE();
