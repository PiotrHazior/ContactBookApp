import json
import mysql.connector

with open("config.json") as config_file:
    config = json.load(config_file)

db = mysql.connector.connect(**config)

if db.is_connected():
    print("Connected to MySQL database!")

cursor=db.cursor()

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Role(
            role_id INT AUTO_INCREMENT PRIMARY KEY,
            role VARCHAR(10) NOT NULL CHECK (role IN ('User', 'Admin'))
        )               
''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person(
            person_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR (50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email NVARCHAR(50) NOT NULL,
            phone INT(11) UNIQUE NOT NULL,
            role_id INT DEFAULT 2,
            FOREIGN KEY (role_id) REFERENCES Role(role_id)                          
        )
''')

cursor.execute("SELECT COUNT(*) FROM Role WHERE role IN ('Admin', 'User')")
role_count = cursor.fetchone()[0]

if role_count < 2:
    cursor.execute("INSERT INTO Role (role) VALUES ('Admin')")
    cursor.execute("INSERT INTO Role (role) VALUES ('User')")


def Register():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
     
    cursor.execute('SELECT phone FROM Person WHERE phone = %s', (phone, ))
    person = cursor.fetchall()
    
    if person:
        print("The given number already exist in the database.")
    
    else:
        cursor.executemany('INSERT INTO Person (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)', [
                    (first_name, last_name, email, phone)
                ]) 
        print("Registration successful.")
    
    

def FindContact():
    phone = input("Please provide your phone number: ")
    cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
    person = cursor.fetchall()
    
    if person:
        print("Data about the person with this number:")
        print(person)
    
    else:
        print('There is no such phone number in the contact database.')       
        
        
        
def UpdateContact():
    phone = input("Please provide person phone number: ")
    cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
    person = cursor.fetchall()
    
    if person:
        print("Data about the person with this phone number:")
        print(person)
        
        update = input("What do you want to change? (first name, last name, email, phone number or role): ")
        
        if update == 'first name':
            new_first_name = input("Please provide new first name: ")
            
            cursor.execute('''
                UPDATE Person
                SET first_name = %s
                WHERE phone = %s
            ''', (new_first_name, phone))

            db.commit()
            
            cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
            person = cursor.fetchone()
            
            print("Update successful.")
            print("Updated data:")
            print(person)
            
        elif update == 'last name':
            new_last_name = input("Please provide new last name: ")
            
            cursor.execute(''' 
                UPDATE Person
                SET last_name = %s
                WHERE phone = %s               
            ''', (new_last_name, phone))
            
            db.commit()
            
            cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
            person = cursor.fetchone()
            
            print("Update successful.")
            print("Updated data:")
            print(person)
            
        elif update == "email":
            new_email = input("Please provide new email: ")
            
            cursor.execute(''' 
                UPDATE Person
                SET email = %s
                WHERE phone = %s               
            ''', (new_email, phone))
            
            db.commit()
            
            cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
            person = cursor.fetchone()
            
            print("Update successful.")
            print("Updated data:")
            print(person)
            
        elif update == "phone number":
            new_phone = input("Please provide new phone number: ")
            cursor.execute('SELECT phone FROM Person WHERE phone = %s', (new_phone, ))
            person = cursor.fetchall()
    
            if person:
                print("The given number already exist in the database.")
            
            else:
                cursor.execute(''' 
                    UPDATE Person
                    SET phone = %s
                    WHERE phone = %s               
                ''', (new_phone, phone))

                db.commit()
            
                cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
                person = cursor.fetchone()
            
                print("Update successful.")
                print("Updated data:")
                print(person)
                
        elif update == 'role':
            new_role = input("Please enter role ('Admin' or 'User'): ")
            
            cursor.execute("SELECT role_id FROM Role WHERE role = %s", (new_role,))
            new_role_id = cursor.fetchone()
            
            cursor.execute(''' 
                    UPDATE Person
                    SET role_id = %s
                    WHERE phone = %s               
                ''', (new_role_id[0], phone))
            
            db.commit()
            
            cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
            person = cursor.fetchone()
            
            print("Update successful.")
            print("Updated data:")
            print(person)
    
    else:
        print('There is no such phone number in the contact database.')   
        
        
        
def DeleteContact():
    phone = input("Please provide phone number: ")
    cursor.execute('SELECT * FROM Person WHERE phone = %s', (phone,))
    person = cursor.fetchall()
    
    if person:
        print("Data about the person with this phone:")
        print(person)
        
        delete = input("Are you sure you want to delete the contact? (Write 'YES' or 'NO'): ")
        
        if delete == 'YES':
            cursor.execute('DELETE FROM Person WHERE phone = %s', (phone,))
            print('Delete successful')
            
        else:
            print('Cancel deleting a contact ...')     
            
    else:
        print('There is no such phone number in the contact database.')   

# DeleteContact()
# FindContact()    
# Register()
# UpdateContact()




cursor.execute('SELECT * FROM Person')
persons = cursor.fetchall()
print("Tabela Person:")
for person in persons:
    print(person)
    
# cursor.execute('DELETE FROM Person')
# cursor.execute("ALTER TABLE Person ADD COLUMN role VARCHAR(10) NOT NULL CHECK (role in ('User', 'Admin'))")
# cursor.execute('ALTER TABLE Person DROP COLUMN role')

# cursor.execute('DELETE FROM Role')

# cursor.execute("DROP TABLE IF EXISTS Person")
# cursor.execute("DROP TABLE IF EXISTS Role")

db.commit()


cursor.close()
db.close()