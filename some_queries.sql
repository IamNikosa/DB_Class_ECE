SELECT * FROM Tickets_In_Resale; -- 822
SELECT ID FROM Ticket T JOIN Tickets_In_Resale TIR ON T.ID = TIR.Ticket_ID; -- 822

SELECT ID FROM Ticket WHERE Still_In_Resale = TRUE;  -- 597
SELECT ID FROM Ticket T JOIN Tickets_In_Resale TIR ON T.ID = TIR.Ticket_ID WHERE Still_In_Resale = TRUE; -- 597

SELECT ID FROM Ticket T JOIN Tickets_In_Resale TIR ON T.ID = TIR.Ticket_ID WHERE Still_In_Resale = FALSE;  -- 225 

SELECT Ticket_ID, Type_ID, Event_ID, Buyer_ID, Is_Resale 
FROM Transaction AS TR JOIN Ticket AS T ON TR.Ticket_ID = T.ID 
WHERE Is_Resale = TRUE AND Still_In_Resale = FALSE;-- 225

SELECT Ticket_ID, Type_ID, Event_ID, Buyer_ID, Is_Resale 
FROM Transaction AS TR JOIN Ticket AS T ON TR.Ticket_ID = T.ID 
WHERE Is_Resale = TRUE; -- 225

SELECT Ticket_ID, Type_ID, Event_ID, Buyer_ID, Is_Resale 
FROM Transaction AS TR JOIN Ticket AS T ON TR.Ticket_ID = T.ID 
WHERE Is_Resale = TRUE AND Still_In_Resale = TRUE;-- 0
