def prompt_generator(prompt_selected: str, args: dict):
    """Generates all prompts needed to run script
    Args:
        prompt_selected (str): prompt to generate, options: ['referral_prompt','fill_in_map', 'static_pa_prompt', 'fill_static_map']
        args (dict): Dictionary contains all necessary arguments
        {
            extracted_fields : dictionary containing the extracted fields from fitz
            extracted_referral : dictionary containing the extracted referral form
            map_json : Gemini generated map of the form and extracted_fields
        }
    """

    def pa_gemini_prompt(extracted_fields: dict):
        return f"""You are an expert medical document processing assistant specializing in Prior Authorization (PA) form analysis and field mapping.Your task is to process and enrich PA form field data with detailed contextual information. 
        <Given Input>
            1. A structured dataset containing PA form field definitions:
                Field names (e.g. CB1, T1)
                Current Values
                Field type string (checkbox, text, etc)
                Field label
                Page number
            2. The prior authorization form PDF document
        <Given Input/>
        <Required Processing>
                For each form field analyze sequentially by page number and:
                    1. extract the implicit question being ask by the field:
                        - For checkboxes: frame the label as a yes/no question
                        - For text fields: frame as an information request
                        - For dates: Specify what event/action the date refers to
                    2. Generate rich contextual information (25 word max) that
                        - The section/category the field belongs to
                        - Whether it's a primary question or sub-question
                        - Whose informaiton is being requested (patient, provider, insurer)
                        - Any dependencies on the other fields
                        - Clinical relevance of the requested information
                    3. Maintain relationships between related field by:
                        - Identifying parent-child relationships between questions
                        - Noting conditional fields that depend on other answers
                        - Preserving the logical flow of the form's struture
        <Required Processing/> 
        <Output Requirements>
            Return a JSON array where each object contains:
                - name: The field identifier (e.g. "CB1", "T1")
                - type: Field type (checkbox, text, etc)
                - page: Page number in the form
                - field_label: Original field label text
                - question: The explicit question being asked by the field
                - context: Rich contextual description (Max 25 words)
                
            Example object structure:
                {{
                    "name": "CB1",
                    "type" : "checkbox",
                    "page" : 2,
                    "field_label" : "Start of Treatment"
                    "question" : "Is this a new treatmentfor the patient?"
                    "context" : "Initial checkbox in treatment timeline section indicating whether patient is beginning a new treatment versus a continuation.
                }}
        </Output Requirements>   
        <Critical Requirements>
            - Every field must have both question and context added
            - Context must be specific and clinically relevant
            - Maintain logical relationship between fields
            - Preserve exact field names and labels
            - Keep context concise but informative (25 words max)
            
            Only output valid JSON.
        </Critical Requirements.>
        <PA_Form_Data>
        {extracted_fields}
        <PA_Form_Data/>
        """

    def pa_static_gemini_map():
        return f"""
            Extract all distinct input areas from the provided PDF where data can be filled in. For each input area, return the following in a JSON array under the key "fields":

            - **page**: The 1-based page number where the input area is located.
            - **bbox**: The bounding box of the input area, formatted as `[x0, y0, x1, y1] expressed in PDF points and **not pixels** (0,0) is bottom left corner of the page, represent (x0, y0) as the bottom-left corner of input field, (x1, y1) is the top-right corner of input field.
            - **field_type**: The most appropriate field type (e.g., "text", "checkbox", "radio", "dropdown", "date", "signature", "address", "phone number", "email"). If a standard type isn't suitable, use "other" and specify in the context. 
            

            An "input area" refers to any region on the form where a user would typically enter text, select an option (like a checkbox or radio button), sign, or interact to provide information. This includes text fields, checkboxes, radio buttons, dropdowns, signature lines, etc. If an input area contains subfields (e.g., a date with separate fields for month, day, and year), ensure each subfield is represented as its own input field. Do not merge multiple fields into a single combined input (e.g., avoid combining mm - dd - yyyy into mm/dd/yyyy). Preserve the original structure of separate inputs where applicable.

            **Output should be a single JSON object with a top-level key "fields" containing an array of input area objects.** Ensure all numerical values are correct. Do not include any additional commentary or markdown outside the JSON.

            ```json
            {{
                "fields": [
                    {{
                        "page": 1,
                        "bbox": [100, 200, 300, 220]
                        "field_type": "text"
                    }},
                    {{
                        "page": 1,
                        "bbox": [150, 250, 170, 270]
                        "field_type": "text",
                    }}
                ]
            }}
            ```
    """

    def add_context_to_static_gemini(map_json: dict):
        return f"""
            Given the provided Prior Authorization form pdf and the specified bounding boxes, identify the input fields located within this bounding box. Then, extract the following information about the specific fields:

            - **name**: The most concise and accurate label or identifier for the field (e.g., "Full Name", "Date of Birth").
            - **page**: The 1-based page number where the input area is located.
            - **question**: The explicit question or instruction associated with the field, exactly as it appears on the form (e.g., "Please provide your full legal name:", "Date you wish to begin employment (MM/DD/YYYY):").
            - **context**: A concise, rich contextual description (maximum 25 words) that clarifies the purpose or usage of the field, especially if not obvious from the name or question (e.g., "Used for official identification purposes.", "Indicates the start date for the proposed project.").
            - **field_type**: The most appropriate field type (e.g., "text", "checkbox", "radio", "dropdown", "date", "signature", "address", "phone number", "email"). If a standard type isn't suitable, use "other" and specify in the context.
            - **bbox**: The bounding box of the input area, formatted as `[x0, y0, x1, y1] expressed in PDF points and **not pixels** (0,0) is bottom left corner of the page, represent (x0, y0) as the bottom-left corner of input field, (x1, y1) is the top-right corner of input field.
            Guidelines:
                -  In the case you run in to a field in the map that is incorrect such as the bbox point to the wrong place in the pdf or not point to a input field, update it if it can be updated else remove it. 
                -  If an input area contains subfields (e.g., a date with separate fields for month, day, and year), ensure each subfield is represented as its own input field. Do not merge multiple fields into a single combined input (e.g., avoid combining mm - dd - yyyy into mm/dd/yyyy). Preserve the original structure of separate inputs where applicable. 
             

             <PA Form fields>
                {map_json}
            <PA Form fields/>

            **Output should be a single JSON object for the extracted fields names fields.** Do not include any additional commentary or markdown outside the JSON.

            ```json
            "fields":  {{
                "name": "Example Field Name",
                "page": 1,
                "question": "Example Question?",
                "context": "Contextual description of the field's purpose.",
                "field_type": "text",
                "bbox" : [x0,y0,x1,y1]
            }}
            ```
    """

    def fill_in_map_gemini(referral_markdown: str, map_json: dict):
        return f"""You are an expert medical document processing assistant specializing in Prior Authorization (PA) form analysis and medical documentation. You given a list of PA form fields with their associated context and questions. Your task is to thoroughly analyze a string containing the ocr extracted information from the referral packet and extract all the relevant information to accurately fill out the PA form.         
    
        <Extracted Referral Packet>
            {referral_markdown}
        <Extracted Referral Packet/>
        
        
        <PA Form fields>
            {map_json}
        <PA Form fields/>
        <Guidelines>
            Please follow the below guidelines:
                1. Carefully review each field in the pa form and understand its requirements.
                2. Match extracted information to the corresponding PA form fields.
                3. If the information is missing or unclear leave the answer as an empty string.
                    - indicate the field that was left empty in the JSON object left_blank along with its reason for being left empty. 
                4. Use exact values and terminology from source documents when possible. 
        <Guidelines/>
        <Output Requirements>
            Return a JSON array containing two object: 
                - Fields: array of fields only containing -- name, page, field_lable, answer in the following format
                
            Example fields object structure:
                {{
                    "name": "CB1",
                    "page" : 2,
                    "field_label" : "Start of Treatment",
                    "Answer" : "Answer to the question based on the extracted referral package" or ""
                }}
            Example left_blank object structure:
                {{
                    "name": "CB1",
                    "page" : 2,
                    "context" : "Original context information".
                    "reason" : "Reason why it was left blank".
                    
                }}
        </Output Requirements>   
        Note: Ensure strict adherence to this format. Do not include any additional fields or commentary outside the JSON
        """

    def fill_in_static_map_gemini(referral_markdown: str, map_json: dict):
        return f"""You are an expert medical document processing assistant specializing in Prior Authorization (PA) form analysis and medical documentation. You given a list of PA form fields of a static form with their associated context, questions and bbox. Your task is to thoroughly analyze a string containing the ocr extracted information from the referral packet and extract all the relevant information to accurately fill out the PA form. 
    
        <Extracted Referral Packet>
            {referral_markdown}
        <Extracted Referral Packet/>
        
        
        <PA Form fields>
            {map_json}
        <PA Form fields/>
        
        <Guidelines>
            Please follow the below guidelines:
                1. Carefully review each field in the pa form and understand its requirements.
                2. Match extracted information to the corresponding PA form fields.
                3. If the information is missing or unclear leave the answer as an empty string.
                    - indicate the field that was left empty in the JSON object left_blank along with its reason for being left empty. 
                4. Use exact values and terminology from source documents when possible. 
        <Guidelines/>
        <Output Requirements>
            Return a JSON response_dict containing two object: 
        "response_dict": {{
                - "fields": array of fields only containing -- name, page, answer, field_type, bbox in the following format
            Example fields object structure:
                {{
                    "name": "Start of Treatment",
                    "page" : 2,
                    "field_type": "text" or "checkbox"
                    "answer" : "Answer to the question based on the extracted referral package" or "",
                    "bbox" : [x0,y0,x1,y1]
                }}
                - "left_blank": array of fields only containing -- name, page, context, reason in the following format
            Example left_blank object structure:
                {{
                    "name": "Start of Treatment",
                    "page" : 2,
                    "context" : "Original context information".
                    "reason" : "Reason why it was left blank".
                }}
                }}
        </Output Requirements>   
        Note: Ensure strict adherence to this format. Do not include any additional fields or commentary outside the JSON
        """

    if prompt_selected == "pa_prompt":
        if "extracted_fields" not in args:
            print("Forgot something in args dict")
            return ""
        return pa_gemini_prompt(extracted_fields=args["extracted_fields"])
    if prompt_selected == "fill_in_map":
        if "extracted_referral" not in args or "map_json" not in args:
            print("Forgot something in args dict")
            return ""
        return fill_in_map_gemini(
            referral_markdown=args["extracted_referral"], map_json=args["map_json"]
        )
    if prompt_selected == "static_pa_prompt":
        # need to figure out prompt to have gemini extract form fields from the pa pdf
        return pa_static_gemini_map()
    if prompt_selected == "static_pa_context_prompt":
        if "map_json" not in args:
            print("Forgot something in args dict")
            return ""
        return add_context_to_static_gemini(map_json=args["map_json"])
    if prompt_selected == "fill_static_map":
        if "extracted_referral" not in args and "map_json" not in args:
            print("Forgot something in args dict")
            return ""
        return fill_in_static_map_gemini(
            referral_markdown=args["extracted_referral"], map_json=args["map_json"]
        )
    else:
        print("Wrong or no prompt option entered")
        return ""
