import pandas as pd
import streamlit as st
import requests
import numpy as np
import lime
import matplotlib.pyplot as plt
from datetime import date


def request_prediction(model_url, payload):
    response = requests.post(model_url, json=payload)
    
    if response.status_code != 200:
        raise Exception(
            'Request failed with status ', response.status_code, '\n', response.text
        )
    return response.json()

def NumberOfDays(date1):
    return (date.today() - date1).days

URL_online = "https://scoring-oc7.herokuapp.com/getPrediction"

def main():

    st.title('Credit Prediction')

    st.write('Please file this form')

    with st.form('credit_form'):

        
            #GENERAL INFO
        st.write('General information')

        #Gender code
        gender = st.selectbox(
            label='Gender of the client',
            options=('Male', 'Female')
        )
        gender_code = 'M' if gender == 'Male' else 'F'

        #Date of birth
        birthday = st.date_input(
            label='Date of birth of the client',
            value=date(1970, 1, 1)
        )
        number_days_birth = -NumberOfDays(birthday)

        #email and phone
        email = st.selectbox(
            label='Did the client provide an email address?',
            options=('Yes', 'No')
        )
        flag_email = 1 if email == 'Yes' else 0

        phone = st.selectbox(
            label='Did the client provide a phone number?',
            options=('Yes', 'No')
        )
        flag_phone = 1 if phone == 'Yes' else 0


        #Family
        family_status = st.selectbox(
            label='Family status of the client',
            options=('Single / not married', 'Married', 'Civil marriage', 'Widow', 'Separated', 'Unknown')
        )

        family_members_count = st.number_input(
            label='Number of family members (Spouse, children) of the client',
            min_value=0
        )

        children_count = st.number_input(
            label='Number of children of the client',
            min_value=0
        )

        #Flag own car
        own_car = st.selectbox(
            label='Does the client own a car?',
            options=('Yes', 'No')
        )
        flag_own_car = 'Y' if own_car == 'Yes' else 'N'

        #Realty
        own_realty = st.selectbox(
            label='Does the client own a house/appartment/realty of any kind?',
            options=('Yes', 'No')
        )
        flag_own_realty = 'Y' if own_car == 'Yes' else 'N'

        housing_type = st.selectbox(
            label='What kind of housing does the client live in?',
            options=('House / apartment', 'Rented apartment', 'With parents', 'Municipal apartment', 'Office apartment', 'Co-op apartment')
        )


            # EDUCATION AND EMPLOYMENT
        st.write('Education and Work')

        education_type = st.selectbox(
            label='Education level',
            options=('Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary', 'Academic degree')
        )

        organization_type = st.selectbox(
            label='Organization type',
            options=(
                'Self-employed', 'School', 'University', 'Kindergarten',
                'Government', 'Security Ministries', 'Legal Services', 'Postal',
                'Military', 'Police', 'Security', 'Services', 
                'Religion', 'Medicine', 'Emergency', 'Electricity',
                'Construction', 'Realtor', 'Housing', 'Hotel',
                'Bank', 'Insurance', 'Mobile', 'Telecom',
                'Culture', 'Advertising', 'Agriculture', 'Restaurant',
                'Cleaning', 'Business Entity Type 1', 'Business Entity Type 2', 'Business Entity Type 3',
                'Transport: type 1', 'Transport: type 2', 'Transport: type 3', 'Transport: type 4',
                'Trade: type 1', 'Trade: type 2', 'Trade: type 3', 'Trade: type 4',
                'Trade: type 5', 'Trade: type 6', 'Trade: type 7', 'Industry: type 1',
                'Industry: type 2', 'Industry: type 3', 'Industry: type 4', 'Industry: type 5',
                'Industry: type 6', 'Industry: type 7', 'Industry: type 8', 'Industry: type 9',
                'Industry: type 10', 'Industry: type 11', 'Industry: type 12', 'Industry: type 13',
                'Other'
            )
        )

        #Income
        annual_income = st.number_input(
            label='Annual income',
            min_value=0
        )

        #Income type
        income_type = st.selectbox(
            label='Income type',
            options=('Working', 'State servant', 'Commercial associate', 'Pensioner',
                    'Unemployed', 'Student', 'Businessman', 'Maternity leave')
        )

        

        #Days employed
        date_employment = st.date_input(
            label='When did the client begin his current employment?',
            value=date(2000, 1, 1)
        )
        days_employed = NumberOfDays(date_employment)


            #CONTRACT
        st.write('Contract information')
        
        #Contract type
        contract_type = st.selectbox(
            label='Contract type',
            options=('Cash loans', 'Revolving loans')
        )

        #Credit amount
        amount_credit = st.number_input(
            label='Requested credit amout',
            min_value=0
        )

        #Goods price
        goods_price = st.number_input(
            label='Price of the good(s) the client wishes to buy',
            min_value=0
        )

        #Annuity
        years_payoff = st.number_input(
            label='Duration of the payoff (years)',
            min_value=1
        )
        annuity = amount_credit / years_payoff

        submitted = st.form_submit_button('Submit')

        if submitted:

            payload = {
                'NAME_CONTRACT_TYPE': contract_type,
                'CODE_GENDER': gender_code,
                'FLAG_OWN_CAR': flag_own_car,
                'FLAG_OWN_REALTY': flag_own_realty,
                'CNT_CHILDREN': children_count,
                'AMT_INCOME_TOTAL': annual_income,
                'AMT_CREDIT': amount_credit,
                'AMT_ANNUITY': annuity,
                'AMT_GOODS_PRICE': goods_price,
                'NAME_INCOME_TYPE': income_type,
                'NAME_EDUCATION_TYPE': education_type,
                'NAME_FAMILY_STATUS': family_status,
                'NAME_HOUSING_TYPE': housing_type,
                'DAYS_BIRTH': number_days_birth,
                'DAYS_EMPLOYED': days_employed,
                'FLAG_MOBIL': flag_phone,
                'FLAG_EMAIL': flag_email,
                'CNT_FAM_MEMBERS': family_members_count,
                'ORGANIZATION_TYPE': organization_type
            }

    response = request_prediction(URL_online, payload)
    if response['Prediction'] == 1:
        st.write('Credit Granted')
    else:
        st.write('Credit denied')

    st.write('Details')







        
if __name__ == '__main__':
    main()