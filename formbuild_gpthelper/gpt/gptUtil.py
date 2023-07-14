import os
from dotenv import load_dotenv
load_dotenv()
import openai
import json
from typing import List

# set the key
openai.api_key = os.environ.get("OPENAI_API_KEY")

def formSpecificationToJson(form_specification : str):
    # form_specification = "form for appliation of driving license"

    # fields_accepted = ["text" , "date" , "textarea" , "radio", "dropdown"]

    example = """
    {
    Header: {
        id: "Id of the field",
        category: "component",
        type: "header",
        headingText: "",
        subHeaderText: "",
    },
    Label: {
        id: "",
        type: "",
        label: "",
    },

    "Text Input": {
        id: "",
        name: "",
        label: "",
        textLabel: "",
        value: "",
        type: "textField",
        charlength: 100
    },
    Text: {
        id: "",
        name: "",
        label: "",
        type: "multiline",
        required: ,
        charlength: ,
        text: "",
    },
    Number: {
        id: "",
        name: "",
        label: "",
        placeholder: "",
        type: "number",
        value: "",
        maximumValue: ,
        minimumValue: ,
    },
    Select: {
        id: "",
        name: "",
        label: "",
        placeholder: "",
        type: "select",
        value: "",
        required: false,
        options: [
            {
                id: "",
                label: "Option label",
                value: "optionValue",
            },
        ]
    },

    "Single Choice": {
        id: ,
        label: "",
        category: "component",
        type: "radio",
        value: "",
        options: [
            {
                id: ,
                title: "Option label",
                value: "optionValue",
            },
        ],
        required: false
    },
    "Multiple Choice": {
        id: "",
        name: "",
        label: "",
        text: "",
        value: [],
        type: "checkbox",
        options: [
            {
                id: ,
                text: "option 1",
                isChecked: false,
            },
            {
                id: ,
                text: "option 2",
                isChecked: false,
            }
        ],
        required: false
    },
    Button: {
        id: "",
        type: "button",
        text: ""
    },
    Date: {
        id: "",
        label: "",
        placeholder: "",
        type: "datepicker",
        value: "",
        minimumDate: "",
        maximumDate: ""
    },
    Time: {
        id: "",
        label: "",
        placeholder: "",
        type: "timepicker",
        value: ""
    },
    Divider: {
        id: "",
        category: "component",
        type: "divider"
    },
    Link: {
        id: "",
        category: "component",
        type: "link",
        linkText: "",
        embeddedLink: "",
        leadingTxt: "",
        trailingTxt: ""
    },
    File: {
        id: "",
        name: "",
        label: "",
        type: "fileUpload",
        value: ""
    },
    Image: {
        id: "",
        name: "",
        label: "",
        type: "image",
        value: ""
    },

    Footer: {
        id: "",
        type: "footer",
        footerText: "text for footer",
        footerLabel: "label for footer"
    }
}
"""

    example_resp = """{
     "fields" : [list of selected fields]
    }"""

    prompt = f"""
    usecase - 'form for - {form_specification}'.
    List of fields are - [Header, Label, Text field, Text, Number, Select, Single Choice, Multiple Choice, Button, Date, Time, Divider, Link, File, Image, Footer]
    Go through the following json of fields to understand the structure of each field - '{example}'
    Generate a form json by picking approriate fields required for the usecase given.
    generate the values for selected fields according to the usecase.
    Do not generate empty values in the form field.
    It is not neccesary to include all the types of fields given.
    response structure must be :
        {example_resp}
    give entire response as a valid JSON.
    """

    print("calling completion api")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": prompt}
            ],
        temperature = 0
    )

    tokens_used = completion['usage']['total_tokens']

    gpt_response = completion["choices"][0]["message"]["content"]

    
    print("response", gpt_response)
    print("tokens used", tokens_used)

    form_fields_json = json.loads(gpt_response)

    return form_fields_json



if __name__ == '__main__':
    form_json = formSpecificationToJson(form_specification= "form for appliation of driving license",
                            fields_accepted = ["text" , "date" , "textarea" , "radio", "dropdown"]
                            )
    print(form_json)