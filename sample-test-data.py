import csv
import random

# Define sections
sections = [
    "Login", 
    "User Management", 
    "Dashboard", 
    "Reports", 
    "Settings", 
    "Profile", 
    "Notifications", 
    "Search", 
    "Cart", 
    "Checkout"
]

# Define common test prefixes
test_prefixes = [
    "Verify that",
    "Check if",
    "Ensure",
    "Validate",
    "Test that",
    "Confirm"
]

# Define test actions by section
section_actions = {
    "Login": [
        "user can log in with valid credentials",
        "login fails with invalid password",
        "forgot password functionality works",
        "user can log in with SSO",
        "login page displays error messages correctly",
        "login works after session timeout",
        "user can log out successfully",
        "remember me functionality works",
        "login page has proper validation for input fields",
        "password strength meter functions correctly",
        "user can reset password through email",
        "login works across different browsers",
        "CAPTCHA appears after multiple failed attempts",
        "login history is recorded correctly",
        "two-factor authentication works"
    ],
    "User Management": [
        "new user can be created successfully",
        "user details can be edited",
        "user can be deleted",
        "admin can assign roles to users",
        "user permissions are applied correctly",
        "bulk user import functions correctly",
        "user groups can be managed",
        "password policies are enforced",
        "user status can be changed",
        "user access can be revoked",
        "user data can be exported",
        "inactive users are flagged automatically",
        "user activity is logged correctly",
        "user search functions properly",
        "duplicate users are prevented"
    ],
    "Dashboard": [
        "all widgets load correctly",
        "data is displayed accurately",
        "widgets can be customized",
        "graphs display real-time data",
        "filters work correctly",
        "dashboard state is saved between sessions",
        "dashboard is responsive on different devices",
        "dashboard exports data in correct formats",
        "charts are interactive",
        "dashboard loads within acceptable time",
        "data is refreshed automatically",
        "alerts display correctly",
        "drag-and-drop functionality works",
        "dashboard preferences can be reset",
        "dashboard remembers user's last view"
    ],
    "Reports": [
        "report can be generated successfully",
        "report data is accurate",
        "report can be exported to PDF",
        "report can be scheduled",
        "filters work correctly on reports",
        "report includes correct date ranges",
        "custom reports can be created",
        "report sharing functions correctly",
        "large reports handle pagination properly",
        "report caching improves performance",
        "report templates can be saved",
        "report shows visualization options",
        "report comments can be added",
        "report comparison feature works",
        "historical reports are accessible"
    ],
    "Settings": [
        "system settings can be updated",
        "changes are saved correctly",
        "default settings can be restored",
        "settings are applied immediately",
        "validation works on settings fields",
        "settings are preserved across sessions",
        "settings can be exported/imported",
        "settings page is accessible to admins only",
        "advanced settings are hidden by default",
        "settings have proper descriptions",
        "dependent settings update accordingly",
        "settings categories are properly organized",
        "settings search works correctly",
        "deprecated settings are properly flagged",
        "settings audit log is maintained"
    ],
    "Profile": [
        "user can update profile information",
        "profile picture can be changed",
        "password can be changed from profile",
        "profile data validation works",
        "privacy settings can be adjusted",
        "language preferences are saved",
        "notification settings work correctly",
        "profile completeness is calculated correctly",
        "connected accounts can be managed",
        "activity history is displayed correctly",
        "profile export includes all required data",
        "profile deletion works as expected",
        "recovery options can be set up",
        "public profile view works correctly",
        "profile verification process works"
    ],
    "Notifications": [
        "email notifications are sent correctly",
        "push notifications work on mobile devices",
        "notification preferences can be set",
        "notifications can be marked as read",
        "notification center displays all alerts",
        "real-time notifications appear instantly",
        "notification templates can be customized",
        "notifications can be filtered by type",
        "batch notifications are processed correctly",
        "notification history is accessible",
        "notification sound settings work",
        "notifications respect quiet hours",
        "notification grouping works correctly",
        "notification counter updates in real-time",
        "notification opt-out functions work"
    ],
    "Search": [
        "search returns relevant results",
        "advanced search filters work correctly",
        "search results are paginated properly",
        "search works with partial keywords",
        "search history is saved",
        "recent searches are displayed",
        "search suggestions appear correctly",
        "no results page displays helpful information",
        "search relevance is accurate",
        "search performance is acceptable",
        "search results can be sorted",
        "search handles special characters",
        "search works across all content types",
        "bulk actions work on search results",
        "search results export functions correctly"
    ],
    "Cart": [
        "items can be added to cart",
        "items can be removed from cart",
        "quantity can be updated",
        "cart total is calculated correctly",
        "promo codes can be applied",
        "cart saves items for logged-in users",
        "guest cart works correctly",
        "cart merges when user logs in",
        "cart shows estimated shipping",
        "cart shows estimated taxes",
        "out-of-stock items are handled properly",
        "cart displays item details correctly",
        "save for later functionality works",
        "cart abandonment email is triggered",
        "cart contents can be shared"
    ],
    "Checkout": [
        "user can complete purchase",
        "payment methods work correctly",
        "order summary displays accurately",
        "shipping options can be selected",
        "address validation works",
        "order confirmation is sent",
        "order history is updated",
        "guest checkout works correctly",
        "express checkout functions properly",
        "payment validation works correctly",
        "order status updates in real-time",
        "invoice is generated correctly",
        "order cancellation works",
        "refund process functions correctly",
        "checkout form validation works"
    ]
}

# Define ticket ID prefixes by section
ticket_prefixes = {
    "Login": "LOGIN-",
    "User Management": "USER-",
    "Dashboard": "DASH-",
    "Reports": "RPT-",
    "Settings": "SET-",
    "Profile": "PROF-",
    "Notifications": "NOTE-",
    "Search": "SRCH-",
    "Cart": "CART-",
    "Checkout": "CHKOUT-"
}

# Define possible test descriptions
descriptions = [
    "This test verifies critical functionality that impacts user experience.",
    "A regression test that must be run after each deployment.",
    "This test ensures data integrity across the system.",
    "Core functionality test that affects multiple user workflows.",
    "This test validates compliance with business requirements.",
    "A user experience validation test.",
    "This test ensures proper integration between systems.",
    "Security-related test case.",
    "Performance validation for key user interaction.",
    "This test verifies proper error handling.",
    "Validation of system behavior under edge conditions.",
    "This test ensures compatibility across different browsers.",
    "A critical path test for the main user journey.",
    "This test verifies correct handling of user inputs.",
    "Validation of system feedback and user notifications.",
    "",  # Some tests might not have descriptions
]

# Create CSV data
csv_data = []

# Add headers
headers = [
    "Rank",
    "Priority",
    "Ticket ID",
    "Section",
    "Test Name",
    "Description",
    "Total Score (100-point)",
    "Raw Score",
    "Test ID",
    "Can it be Automated",
    "Regression Frequency",
    "Customer Impact",
    "Manual Test Effort",
    "Automation Complexity",
    "Existing Framework",
    "Angular Framework",
    "Repetitive"
]

# Generate 150 test cases
for i in range(1, 251):
    # Determine if this test will be marked as "Won't Automate"
    can_be_automated = random.choices([1, 3, 5], weights=[5, 10, 85])[0]  # 5% won't automate, 10% maybe, 85% yes
    
    # Choose a section
    section = random.choice(sections)
    
    # Generate a test name
    prefix = random.choice(test_prefixes)
    action = random.choice(section_actions[section])
    test_name = f"{prefix} {action}"
    
    # Generate a ticket ID
    ticket_id = f"{ticket_prefixes[section]}{random.randint(1000, 9999)}"
    
    # Generate a description
    description = random.choice(descriptions)
    
    # If this test won't be automated, all other factors don't matter
    if can_be_automated == 1:  # No (Won't Automate)
        # Set all other factors to middle value (won't be used)
        regression_frequency = 3
        customer_impact = 3
        manual_test_effort = 3
        automation_complexity = 3
        existing_framework = 3
        angular_framework = 3
        repetitive = 3
        
        # Set scores to 0
        raw_score = 0
        total_score = 0
        priority = "Won't Automate"
    else:
        # Generate factor scores - make some correlation between factors
        regression_frequency = random.choices([1, 3, 5], weights=[20, 50, 30])[0]
        customer_impact = random.choices([1, 3, 5], weights=[15, 55, 30])[0]
        
        # Tests with high regression frequency and customer impact tend to have higher manual effort
        if regression_frequency >= 3 and customer_impact >= 3:
            manual_test_effort_weights = [10, 40, 50]  # More likely to be high effort
        else:
            manual_test_effort_weights = [40, 40, 20]  # More likely to be low effort
        
        manual_test_effort = random.choices([1, 3, 5], weights=manual_test_effort_weights)[0]
        
        # Repetitive tests might be easier to automate
        repetitive = random.choices([1, 3, 5], weights=[20, 40, 40])[0]
        
        # Automation complexity (5 = easy to automate, 1 = difficult)
        if repetitive >= 3:
            automation_complexity_weights = [10, 40, 50]  # More likely to be easy to automate
        else:
            automation_complexity_weights = [40, 40, 20]  # More likely to be complex
        
        automation_complexity = random.choices([1, 3, 5], weights=automation_complexity_weights)[0]
        
        # Existing framework and Angular framework are somewhat independent
        existing_framework = random.choices([1, 3, 5], weights=[30, 40, 30])[0]
        angular_framework = random.choices([1, 3, 5], weights=[20, 30, 50])[0]
        
        # Calculate raw score
        # Weights: Regression (3), Impact (3), Manual Effort (2), Complexity (2), Existing (2), Angular (1), Repetitive (1)
        raw_score = (
            regression_frequency * 3 +
            customer_impact * 3 +
            manual_test_effort * 2 +
            automation_complexity * 2 +
            existing_framework * 2 +
            angular_framework * 1 +
            repetitive * 1
        )
        
        # Calculate total score (normalized to 100)
        # Maximum possible raw score: 5*(3+3+2+2+2+1+1) = 5*14 = 70
        total_score = round((raw_score / 70) * 100, 1)
        
        # Determine priority based on score
        if total_score >= 85:
            priority = "Highest"
        elif total_score >= 70:
            priority = "High"
        elif total_score >= 55:
            priority = "Medium"
        elif total_score >= 40:
            priority = "Low"
        else:
            priority = "Lowest"
    
    # Create CSV row
    row = [
        i,  # Rank
        priority,
        ticket_id,
        section,
        test_name,
        description,
        total_score,
        raw_score,
        i,  # Test ID
        can_be_automated,
        regression_frequency,
        customer_impact,
        manual_test_effort,
        automation_complexity,
        existing_framework,
        angular_framework,
        repetitive
    ]
    
    csv_data.append(row)

# Write to CSV file
with open('testprior.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(csv_data)

print(f"Created testprior.csv with {len(csv_data)} test cases")
