import datetime
import random
import faker


# returns first letter in uppercase of sex
def randomSex():
    sex = ['M', 'F']
    option = random.randrange(0, 2)
    return sex[option]

# returns date in format 'yyyy-mm-dd'


def randomDate():
    day = random.randrange(1, 32)
    mounth = random.randrange(1, 13)
    year = random.randrange(1900, 2019)
    while True:
        day = random.randrange(1, 32)
        mounth = random.randrange(1, 13)
        year = random.randrange(1900, 2019)
        try:
            datetime.date(year, mounth, day)
            break
        except:
            pass
    date = '{}-{}-{}'.format(year, mounth, day)
    return date


# returns a full name
def randomName():
    return faker.Faker().name()


# returns a random text
def randomText():
    return faker.Faker().text()


# returns a random boolean
def randomBoolean():
    option = random.randrange(0, 2)
    return bool(option)


# returns a integer number
def randomInteger(start, end):
    number = random.randrange(start, end + 1)
    return number


# returns a float number to 2 decimal places
def randomFloat(start, end): 
    number = random.uniform(start, end + 0.01)
    number = round(number, 2)
    return number


