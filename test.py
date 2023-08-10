def on_create_party_registration(name, email, phone):
    # This function is triggered when a new party registration is created.
    # It could perform tasks such as saving registration data to a database,
    # sending confirmation emails, or performing validation checks.

    # Replace 'database' with your actual database handling code.
    registration_data = {
        'name': name,
        'email': email,
        'phone': phone
    }
    # Your code to save registration_data to the database

    # Replace 'email_sender' with your actual email sending library.
    # For example, you might use Python's built-in smtplib, SendGrid, or any other email service.
    email_subject = "Registration Confirmation"
    email_body = "Thank you for registering for the party!"
    # Your code to send an email with the provided subject and body to the given email address.

    # Perform any other necessary tasks
    # ...

    # Return a success message or relevant response
    return "Registration successful!"


# Example usage
registration_name = "John Doe"
registration_email = "johndoe@example.com"
registration_phone = "123-456-7890"

result = on_create_party_registration(
    name=registration_name,
    email=registration_email,
    phone=registration_phone
)
print(result)
