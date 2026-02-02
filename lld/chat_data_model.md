# Core Data Model
1. Users and Companies
- App_user: (id, name, email, external_id) - end customer
- Company: (id, name, plan_type) - tenant
- Admin: (id, name, company_id, role) - the support agent/employee

2. Conversations (the container): Conversation belongs to a company and user
conversation_id: PK
app_user_id: FK to app_user
company_id: FK to company
status: OPEN, CLOSED, SNOOZED
assigned_to: nullabel FK to admin (current owner)
created_at: timestamp

Question : why assigned_to when app_user_id is already present?

3. Conversation participants. since employees can join in between. need to track who is subscribed to the thread for notification/access, separate from the assigned_to field.
- conversation_id
- admin_id
- joined_at

4. Messages. 
message_id: UUID
conversation_id: uuid. fk to conversation
author_id: id of the user or the admin
author_type: enum - user, admin, bot
body: text
content_type: text, image, block

Question: if it is image then will we have url also?

5. Broadcasting. sending 1 message to 100k users requires different data model, to avoid storing "hello" strings in the messages table
- Campaign: Stores the template content ("hey {{first_name}}, check this out!")
- Campaign audience: defines the query on who receives it. For example: user signed up > 7 days ago
- conversation injection: instead of inserting a row into messages, you create a lightweight link.
    - when the user opens their chat, system checks for active campaigns targeted at them
    - if user replies to broadcast. then you materialise the real row in messages table and start a standard conversation

6. Production and scale considerations
Database choice: Postgres
Messages: Cassandra, Write heave no-sql stores handle the high volume of chat logs better than sql, and scale horizontally by conversation id

Real time delivery:
Websockets
pub/sub (redis/kafka): 

Elastic search for seach 