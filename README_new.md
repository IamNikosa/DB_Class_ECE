# Pulse University Festival Database 

## Project Scope
The project models a complex international music festival using a relational database, with features including:

- Annual festivals at different global locations
- Multiple stages and event performances
- Detailed performer tracking (solo, bands, subgenres)
- Ticketing system with purchase, resale, and capacity validation
- Staff assignment and scheduling logic (with coverage % rules)
- Real-time validation with triggers (e.g., no double booking, no overbooking)
- Visitor interest queues, waitlisting, and automatic resale matchmaking
- Reviews using Likert-based scoring criteria
- Image support for all key entities (e.g., festivals, artists, stages)

## Key Features
### Realistic Constraints & Logic:
- Performers can’t perform in overlapping slots or more than 3 consecutive years.
- Automatic validation of performance spacing (5–30 min).
- Resale queue FIFO logic with buyer-seller matching.
- Ticket VIP caps at 10% of stage capacity.
- Activation of ticket upon scan prevents reuse.

### Triggers & Procedures:
- Custom triggers (capacity checks, sale activation, ticket reuse).
- Modular procedures (e.g., resale handling, ticket scan, staff auto-assignment).

### Optimization:
- Indexes for all major join paths.
- Query plan analysis and forced index testing for Q04 and Q06.
- Views for participation stats, ratings, revenue.

## Directory Structure

- diagrams/: Visual design of the system (E/R + relational)
- sql/: DDL + data loading scripts + queries and their answers
- code/: Python code for synthetic data generation and testing queries
- docs/: PDF report including optimizations, query plans, and conclusions

## Contributors
- Aggelis Manthos 03122027
- Athanasopoulos Nikolaos 03122101
- Papadimitriou Niki 03122005