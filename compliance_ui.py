import streamlit as st
import tempfile
import os
import sys
from io import StringIO
from compliance_checker import check_compliance, guidelines, contract_text

def main():
    st.title("Contract Compliance Checker")
    st.write("Upload your contract and guidelines documents to check compliance")

    # File uploaders
    contract_file = st.file_uploader("Upload Contract (PDF)", type=['pdf'])
    guidelines_file = st.file_uploader("Upload Guidelines (PDF)", type=['pdf'])

    if contract_file and guidelines_file:
        # Create a button to start processing
        if st.button("Check Compliance"):
            with st.spinner("Analyzing documents..."):
                try:
                    # Capture the output from compliance_checker
                    old_stdout = sys.stdout
                    result_output = StringIO()
                    sys.stdout = result_output
                    
                    # Run compliance checks
                    for i, guideline in enumerate(guidelines, 1):
                        result = check_compliance(guideline)
                        print(f"Guideline {i}: {result}")
                    
                    # Restore stdout and get the results
                    sys.stdout = old_stdout
                    results = result_output.getvalue().strip().split('\n')
                    
                    # Display results
                    st.subheader("Compliance Results:")
                    
                    for result in results:
                        guideline_num = result.split(':')[0]
                        compliance = result.split(':')[1].strip()
                        
                        if compliance == "YES":
                            st.success(f"{guideline_num}: ✅ Compliant\n{guidelines[int(guideline_num.split()[1])-1]}")
                        else:
                            st.error(f"{guideline_num}: ❌ Non-Compliant\n{guidelines[int(guideline_num.split()[1])-1]}")
                    
                    st.success("Analysis completed!")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 