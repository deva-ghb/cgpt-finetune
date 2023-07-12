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
        headingAlignment: "left",
        headingSize: "default",
        headerLogo: "",
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/header.svg",
    },
    Label: {
        id: "Id of the field",
        category: "component",
        type: "label",
        label: "Label",
        labelTypeOptions: [
            {
                label: "Normal Text",
                value: "p",
            },
            { label: "Heading - large", value: "h1" },
            { label: "Heading - medium", value: "h2" },
            { label: "Heading - small", value: "h3" },
        ],
        labelType: "",
        labelAlign: "Auto",
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/label.svg",
    },

    "Text Input": {
        id: "",
        name: "",
        label: "",
        textLabel: "",
        value: "",
        category: "component",
        type: "textField",
        required: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        textfieldOptions: [
           {
                label: "Text Input",
                value: "Text Field",
            },
            {
                label: "Email",
                value: "Email",
            },
            {
                label: "Password",
                value: "Password",
            },
        ],
        imageURL: "/assets/formbuilder/text-field.svg"
    },
    Text: {
        id: "",
        name: "",
        label: "",
        category: "component",
        type: "multiline",
        required: ,
        charlength: ,
        text: "",
        customClass: 12,
        options: [
            {
                label: "Normal Text",
                value: "p",
            },
            { label: "Heading - large", value: "h1" },
            { label: "Heading - medium", value: "h2" },
            { label: "Heading - small", value: "h3" },
        ],
        width: 12,
        imageURL: "/assets/formbuilder/txt-input.svg",
    },
    Number: {
        id: ,
        name: "",
        label: "",
        placeholder: "",
        category: "component",
        type: "number",
        value: "",
        required: false,
        maximumValue: ,
        minimumValue: ,
        stepValue: 0,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/Numbers.svg",
    },
    Select: {
        id: "",
        name: "",
        label: "",
        category: "component",
        placeholder: "",
        type: "select",
        value: "",
        required: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        options: [
            {
                id: "",
                label: "Option label",
                value: "optionValue",
            },
        ],
        imageURL: "/assets/formbuilder/select.svg",
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
        required: false,
        spreadToCloumns: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/radio.svg",
    },
    "Multiple Choice": {
        id: "",
        name: "",
        label: "",
        text: "",
        value: [],
        category: "component",
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
            },
            {
                id:,
                text: "option 3",
                isChecked: false,
            },
        ],
        required: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/checkbox2.svg",
    },
    Button: {
        id: ,
        category: "component",
        type: "button",
        text: "",
        btnAlignment: "Auto",
        billingText: "",
        required: false,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/Submit Button.svg",
    },
    Date: {
        id: ,
        label: "",
        placeholder: "",
        category: "component",
        type: "datepicker",
        value: "",
        dontAllowPastDate: false,
        dontAllowFutureDate: false,
        minimumDate: "",
        maximumDate: "",
        required: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/calendar.svg",
    },
    Time: {
        id: "",
        label: "",
        placeholder: "",
        type: "timepicker",
        value: "",
        dontAllowPastTimes: false,
        dontAllowFutureTimes: false,
        minimumTime: "",
        maximumTime: "",
        required: false,
        charlength: 100,
        width: 12,
        imageURL: "url to clock icon",
    },
    Divider: {
        id: "",
        category: "component",
        type: "divider",
        dividerStyle: "",
        dividerColor: "",
        required: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/divided.svg",
    },
    Link: {
        id: ,
        category: "component",
        type: "link",
        linkText: "",
        embeddedLink: "",
        leadingTxt: "",
        trailingTxt: "",
        required: false,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/link.svg",
    },
    File: {
        id: "",
        category: "component",
        name: "",
        label: "",
        type: "fileUpload",
        value: "",
        required: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/files.svg",
    },
    Image: {
        id: "",
        category: "component",
        name: "",
        label: "",
        type: "image",
        value: "",
        imageWidth: 60,
        imageHeight: 60,
        imageAlignment: "Auto",
        required: false,
        charlength: 100,
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/photo.svg",
    },

    Footer: {
        id: "",
        category: "component",
        type: "footer",
        footerText: "text for footer",
        footerLabel: "label for footer",
        footerAlignment: "left",
        headingSize: "default",
        customClass: 12,
        width: 12,
        imageURL: "/assets/formbuilder/footer.png",
    }
}
"""

    example_resp = """{
     "fields" : [list of selected fields]
    }"""

    prompt = f"""
    usecase - '{form_specification}'.
    List of fields are - [Header, Label, Text field, Text, Number, Select, Single Choice, Multiple Choice, Button, Date, Time, Divider, Link, File, Image, Footer]
    Go through the following json of fields to understand the structure of each field - '{example}'
    Generate a form json by picking approriate fields required for the usecase.
    generate the values for selected fields accoring to usecase.
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

    form_fields_json = json.loads(gpt_response)

    return form_fields_json



if __name__ == '__main__':
    form_json = formSpecificationToJson(form_specification= "form for appliation of driving license",
                            fields_accepted = ["text" , "date" , "textarea" , "radio", "dropdown"]
                            )
    print(form_json)