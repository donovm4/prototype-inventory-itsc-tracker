# User Test Cases

> [!IMPORTANT]
> These were the initial user test cases identified when meeting with the ITSC team. After extensive conversations, I consolidated the most important 20 processes that the team and I believed the application should handle.

## Sign-in and Home

1.	User enters an invalid email / message appears for invalid email
2.	User enters an invalid password / message appears for invalid password
3.	User clicks `Login` / User is logged in, with success message
4.	User clicks `Logout` / User is logged out and sent to sign-in page
5.	User clicks `Close` on ticket / ticket should delete from database
6.	User clicks `<user>@<address>` / Outlook should open with proper mailing.

## Navigation

7.	User clicks `Logout` / User is logged out and sent to sign-in page
8.	User clicks `Calendar` link / application properly frames the Mount`s academic calendar
9.	User clicks `View users` link / users page opens in new tab
10.	User clicks links in nav-bar / User is directed to respective pages

## Sign Up Page

11.	User submits names least than 4 characters / Error message displayed
12.	User submits email without `@` symbol / Error message displayed
13.	User submits password less than 5 in length / Error message displayed
14.	`Sign-up` page should only be available to managers and lead manager
15.	User clicks `Submit` / new user is created in database, User returned to home page

## Item Registration

16.	User clicks `Submit` / Item gets added to database, appears in respective section below
17.	User clicks `Notify` / Outlook opens with proper mailing
View Users
18.	User clicks `Go To Top` / page reloads back to top
19.	User clicks `Close` on users / user is deleted from database

## Equipment Log

20.	User clicks `Close` on equipment / equipment is signed back in, or deleted from database if signed in

