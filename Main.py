import json
import mysql.connector

with open("config.json") as config_file:
    config = json.load(config_file)

db = mysql.connector.connect(**config)

if db.is_connected():
    print("Connected to MySQL database!")

cursor=db.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS Person(
            person_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR (50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email NVARCHAR(50) NOT NULL,
            phone INT(11) UNIQUE NOT NULL                              
        )
''')


def CreateContact():
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
        
        update = input("What do you want to change? (first name, last name, email or phone number): ")
        
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
# CreateContact()
# UpdateContact()

cursor.execute('SELECT * FROM Person')
persons = cursor.fetchall()
print("Tabela Person:")
for person in persons:
    print(person)
    


db.commit()


cursor.close()
db.close()