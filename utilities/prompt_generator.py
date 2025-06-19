def prompt_generator(prompt_selected: str, args: dict):
    """Generates all prompts needed to run script
    Args:
        prompt_selected (str): prompt to generate, options: ['pa_prompt', 'referral_prompt','fill_in_map']
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
                - context: Rich contextdual description (Max 25 words)
                
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

    def referral_mistral_prompt():
        return f"""You are an expert medical document processing assistant specializing in extracting information from referral packets that contain necessary information to fill out a prior authorization form. You will be given the referral form and using OCR extract all medical data that is found on the documents with all relevant context. 
        <Given Input>
            1.  Uploaded and signed pdf, Referral Packet
        <Given Input/>
        <Required Processing>
            Ensure to analyze for following:
                1. Start of Treatment or Continuation of therapy
                2. Patient Information
                3. Insurance Information
                4. Prescriber Information
                5. Dispensing and Administration Information
                6. Product Infroamtion
                7. Diagnosis information
                8. All clinical information present in document
                9. All prior treatments attempted, if stopped state reason why it was stopped
            Ensure to include all relevant dates.
        <Required Processing/> 
        <Output Requirements>
            Return a JSON containing all extracted information. 
            Example object structure:
                {{
                    "extracted_information": "Paragraphs of all information extracted".
                }}
        </Output Requirements>   
        <Critical Requirements>
            - All data extracted and returned must be present in the original document. 
            - DO NOT HALLUCINATE INFORMATION.
            - Only output valid JSON.
        </Critical Requirements.>
        """

    def fill_in_map_gemini(referral_json: dict, map_json: dict):
        # TODO prompt to fill in map with gemini using information extracted from mistral (may have to keep an eye on tokens when passing all info)
        pass

    if prompt_selected == "pa_prompt":
        if "extracted_fields" not in args:
            print("Forgot something in args dict")
            return ""
        return pa_gemini_prompt(extracted_fields=args["extracted_fields"])
    if prompt_selected == "referral_prompt":
        return referral_mistral_prompt()
    if prompt_selected == "fill_in_map":
        if "extracted_referral" not in args or "map_json" not in args:
            print("Forgot something in args dict")
            return ""
        return fill_in_map_gemini(
            referral_json=args["extracted_referral"], map_json=args["map_json"]
        )
    else:
        print("Wrong or no prompt option entered")
        return ""
