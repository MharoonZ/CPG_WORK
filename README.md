# Heart Failure Guidelines Recommendation System

## Overview

The Heart Failure Guidelines Recommendation System is an AI-powered clinical decision support tool that helps healthcare providers make evidence-based decisions for heart failure patients. The system processes patient information in natural language format and provides recommendations based on the 2022 AHA/ACC/HFSA Heart Failure Guidelines.

### Purpose

This system aims to:
- Reduce cognitive load on healthcare providers by automating guideline interpretation
- Ensure consistent application of evidence-based recommendations
- Improve patient care through standardized guideline adherence
- Provide immediate access to complex guideline recommendations
- Support clinical decision-making with clear rationale and evidence levels

## Features

### Natural Language Processing
- Accepts patient information in natural language format
- Handles various input styles and medical terminology
- Supports both structured and unstructured clinical notes
- Processes complex medical abbreviations and common variations

### Intelligent Data Extraction
Automatically extracts and validates key clinical parameters:
- **Demographics**:
  - Age and sex
  - Body weight and height (if provided)
  - Race/ethnicity (if relevant to treatment decisions)
- **Cardiac Parameters**:
  - LVEF (Left Ventricular Ejection Fraction)
  - NYHA Class (I-IV)
  - Heart failure stage (A-D)
  - Heart failure type (HFrEF, HFpEF, HFmrEF)
- **Medications**:
  - Current medications with dosages
  - Medication frequency and timing
  - Recent medication changes
  - Medication allergies or intolerances
- **Laboratory Values**:
  - Potassium levels
  - eGFR (estimated Glomerular Filtration Rate)
  - Sodium levels
  - BNP/NT-proBNP (if available)
  - Other relevant lab values
- **Comorbidities and History**:
  - Diabetes mellitus
  - Chronic kidney disease
  - Hypertension
  - Previous angioedema
  - Other relevant conditions

### Evidence-Based Recommendations
- Generates recommendations based on the 2022 AHA/ACC/HFSA Heart Failure Guidelines
- Includes Class of Recommendation (COR) and Level of Evidence (LOE)
- Provides specific medication dosing and titration schedules
- Includes monitoring recommendations and follow-up parameters
- Highlights contraindications and precautions

### Input Methods
1. **Interactive Console Input**:
   - Real-time input processing
   - Multi-line input support
   - Immediate feedback on input validation
   - Clear error messages for invalid inputs

2. **Direct Text Input**:
   - Command-line argument support
   - Quoted string processing
   - Special character handling
   - Input validation

3. **File-Based Input**:
   - Support for various text file formats
   - Batch processing capability
   - File encoding detection
   - Error handling for file operations

### Output Features
- **Rich Text Formatting**:
  - Color-coded sections for better readability
  - Hierarchical information structure
  - Clear separation of different recommendation types
  - Highlighted important warnings and contraindications

- **Comprehensive Logging**:
  - Detailed debug information
  - Input validation logs
  - API interaction logs
  - Error tracking and reporting
  - Performance metrics

- **Error Handling**:
  - Graceful API failure recovery
  - Static recommendation fallback
  - Clear error messages
  - Input validation feedback

## Technical Architecture

### Core Components

1. **Text Extractor (`text_extractor.py`)**
   - **Natural Language Processing**:
     - Regular expression pattern matching
     - Medical terminology normalization
     - Context-aware parameter extraction
     - Unit conversion and standardization
   - **Data Validation**:
     - Range checking for numerical values
     - Medication name verification
     - Unit consistency validation
     - Required parameter verification

2. **Guideline Processor (`guideline_processor.py`)**
   - **Guideline Management**:
     - Structured guideline storage
     - Version control for guidelines
     - Section-based organization
     - Cross-reference handling
   - **Recommendation Processing**:
     - Context-aware section selection
     - Evidence level tracking
     - Contraindication checking
     - Drug interaction verification

3. **LLM Interface (`llm_interface.py`)**
   - **OpenAI Integration**:
     - GPT-4 model utilization
     - Context-aware prompting
     - Response formatting
     - Error handling
   - **Fallback System**:
     - Static recommendation database
     - Offline recommendation generation
     - Graceful degradation
     - Error recovery

4. **Main Application (`main.py`)**
   - **User Interface**:
     - Command-line argument parsing
     - Interactive input handling
     - Output formatting
     - Progress indication
   - **System Management**:
     - Configuration loading
     - Environment setup
     - Resource management
     - Error handling

### Dependencies

- **Core Requirements**:
  - Python 3.10 or higher
  - OpenAI API access (GPT-4)
  - Internet connection for API calls

- **Python Packages**:
  - `openai`: GPT-4 API integration
  - `python-dotenv`: Environment variable management
  - `rich`: Enhanced console output
  - `logging`: System monitoring
  - `typing`: Type hints and validation
  - `argparse`: Command-line interface

## Installation

1. **Repository Setup**:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. **Environment Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Dependency Installation**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   Create `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   LOG_LEVEL=INFO  # Optional: DEBUG, INFO, WARNING, ERROR
   ```

## Usage

### Basic Usage

1. **Interactive Mode**:
   ```bash
   python main.py
   ```
   - Enter patient information when prompted
   - Use Ctrl+D (Linux/Mac) or Ctrl+Z (Windows) to finish input
   - View formatted recommendations

2. **Direct Input Mode**:
   ```bash
   python main.py -i "65-year-old male with HFrEF, LVEF 35%, NYHA Class II symptoms..."
   ```
   - Provide patient information as a command-line argument
   - Use quotes for multi-line input
   - View immediate recommendations

3. **File Input Mode**:
   ```bash
   python main.py -f patient_case.txt
   ```
   - Process patient information from a text file
   - Support for multiple cases in one file
   - Batch processing capability

### Advanced Usage

1. **Verbose Logging**:
   ```bash
   python main.py -v -i "patient information"
   ```
   - Enable detailed logging
   - View system processing steps
   - Debug information output

2. **Guideline Preprocessing**:
   ```bash
   python main.py -p
   ```
   - Update guideline database
   - Process new guideline sections
   - Optimize recommendation generation

### Input Format Guidelines

1. **Required Information**:
   ```
   Age and sex
   Heart failure type (HFrEF, HFpEF, HFmrEF)
   LVEF percentage
   NYHA Class
   Current medications with dosages
   Key lab values (K+, eGFR)
   ```

2. **Optional Information**:
   ```
   Comorbidities
   Previous adverse reactions
   Current symptoms
   Recent hospitalizations
   Additional lab values
   ```

### Example Inputs

1. **Basic Case**:
   ```
   65-year-old male with HFrEF, LVEF 35%, NYHA Class II symptoms. Currently on Lisinopril 10mg daily and Metoprolol Succinate 50mg daily. K+ 4.1 mEq/L, eGFR 55 mL/min/1.73m².
   ```

2. **Complex Case**:
   ```
   72-year-old female with HFrEF, LVEF 28%, NYHA Class III symptoms. History of diabetes and CKD. Currently on Lisinopril 20mg daily, Metoprolol Succinate 100mg daily, and Furosemide 40mg daily. K+ 4.8 mEq/L, eGFR 32 mL/min/1.73m². No history of angioedema.
   ```

### Example Output

```
================================================================================
RECOMMENDATION BASED ON 2022 AHA/ACC/HFSA HEART FAILURE GUIDELINES
================================================================================

PATIENT SUMMARY:
- 65-year-old male with Stage C Heart Failure with Reduced Ejection Fraction (HFrEF)
- LVEF 35%, NYHA Class II symptoms
- Currently on Lisinopril 10mg daily, Metoprolol Succinate 50mg daily
- Labs: K+ 4.1 mEq/L, eGFR 55 mL/min/1.73m²
- No history of angioedema

RECOMMENDATIONS:

1. Consider switching ACEi (Lisinopril) to ARNi (Sacubitril/Valsartan)
   - Class 1, Level of Evidence B-R (Section 7.3.1, Recommendation 4)
   - Rationale: Patient has HFrEF with NYHA class II symptoms, is currently on an ACEi, and has no history of angioedema
   - Start with 49/51 mg twice daily and titrate to target dose of 97/103 mg twice daily as tolerated
   - Monitor for hypotension, hyperkalemia, and renal function
   - Avoid in patients with history of angioedema

2. Add Mineralocorticoid Receptor Antagonist (MRA)
   - Class 1, Level of Evidence A (Section 7.3.3, Recommendation 1)
   - Rationale: Patient has HFrEF with NYHA class II symptoms, eGFR >30 mL/min/1.73m², and K+ <5.0 mEq/L
   - Start with Spironolactone 25 mg daily or Eplerenone 25 mg daily
   - Monitor potassium and renal function at initiation and regularly thereafter
   - Titrate based on tolerance and lab values

3. Add SGLT2 inhibitor
   - Class 1, Level of Evidence A (Section 7.3.4, Recommendation 1)
   - Rationale: Patient has symptomatic HFrEF
   - Dose: Dapagliflozin 10 mg daily or Empagliflozin 10 mg daily
   - Benefit occurs irrespective of presence of diabetes
   - Monitor for volume depletion and genital mycotic infections

4. Optimize Beta-Blocker dosing
   - Current dose of Metoprolol Succinate (50 mg daily) is below target dose
   - Consider uptitration to target dose of 200 mg daily as tolerated
   - Monitor for bradycardia and hypotension during uptitration
   - Titrate every 2 weeks if stable

ADDITIONAL RECOMMENDATIONS:
- Continue heart failure education and self-care support
- Ensure vaccination against respiratory illnesses
- Consider screening for depression and social isolation
- Avoid excessive sodium intake
- Regular follow-up for medication titration and monitoring
```

## Development

### Project Structure

```
.
├── main.py              # Main application entry point
├── text_extractor.py    # Patient data extraction module
├── guideline_processor.py # Guidelines processing module
├── llm_interface.py     # OpenAI API integration
├── utils.py            # Utility functions
├── requirements.txt    # Project dependencies
└── .env               # Environment variables (not tracked in git)
```

### Adding New Features

1. **New Clinical Parameters**:
   - Add pattern matching in `text_extractor.py`
   - Update patient data structure
   - Modify recommendation logic in `llm_interface.py`

2. **New Guidelines**:
   - Add new sections to `guidelines.json`
   - Update preprocessing logic in `guideline_processor.py`
   - Modify recommendation generation in `llm_interface.py`

### Testing

1. **Unit Tests**:
   - Test individual components
   - Verify data extraction
   - Validate guideline processing
   - Check API integration

2. **Integration Tests**:
   - End-to-end testing
   - Input validation
   - Output formatting
   - Error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines

1. **Code Style**:
   - Follow PEP 8 guidelines
   - Use type hints
   - Document functions and classes
   - Write unit tests

2. **Documentation**:
   - Update README for new features
   - Document API changes
   - Include usage examples
   - Add inline comments

## License

[Specify your license here]

## Acknowledgments

- 2022 AHA/ACC/HFSA Heart Failure Guidelines
- OpenAI for GPT-4 API
- Contributors and maintainers

## Project Goals and Implementation

### Primary Goals

1. **Clinical Decision Support**
   - Automate guideline interpretation for healthcare providers
   - Reduce cognitive load in complex decision-making
   - Ensure consistent application of evidence-based recommendations
   - Improve patient care through standardized guideline adherence

2. **Technical Objectives**
   - Create a robust natural language processing system for medical text
   - Implement accurate clinical parameter extraction
   - Develop reliable recommendation generation
   - Ensure system reliability and error handling

### Implementation Details

1. **Core System Development**
   - **Text Processing Pipeline**:
     - Implemented regex-based pattern matching for clinical parameters
     - Developed context-aware medical terminology processing
     - Created robust error handling for input validation
     - Built unit conversion and standardization system

   - **Guideline Management**:
     - Structured the 2022 AHA/ACC/HFSA Heart Failure Guidelines
     - Implemented section-based organization
     - Created cross-reference system for recommendations
     - Developed version control for guideline updates

   - **Recommendation Engine**:
     - Integrated OpenAI GPT-4 for intelligent processing
     - Implemented fallback mechanisms for API failures
     - Created static recommendation database
     - Developed context-aware recommendation selection

2. **User Interface Development**
   - **Command-Line Interface**:
     - Implemented multiple input methods
     - Created rich text formatting
     - Developed progress indication
     - Built comprehensive error messaging

   - **Input Processing**:
     - Interactive console input
     - Direct text input via command line
     - File-based input with batch processing
     - Input validation and error handling

3. **System Integration**
   - **Component Integration**:
     - Connected text extraction with guideline processing
     - Integrated LLM interface with recommendation generation
     - Implemented logging and monitoring
     - Created configuration management

   - **Error Handling**:
     - Developed graceful API failure recovery
     - Implemented static recommendation fallback
     - Created comprehensive error logging
     - Built user-friendly error messages

### Technologies Used

1. **Programming Languages and Frameworks**
   - Python 3.10+ for core development
   - Regular expressions for pattern matching
   - Type hints for code reliability
   - Object-oriented programming principles

2. **External Services and APIs**
   - OpenAI GPT-4 for recommendation generation
   - Rich library for console formatting
   - Python-dotenv for environment management
   - Logging framework for system monitoring

3. **Development Tools**
   - Git for version control
   - Virtual environment for dependency management
   - Logging for debugging and monitoring
   - Type checking for code quality

### Success Metrics and Results

1. **Functional Success**
   - Successfully processes natural language input
   - Accurately extracts clinical parameters
   - Generates evidence-based recommendations
   - Handles various input formats reliably

2. **Technical Performance**
   - Robust error handling and recovery
   - Efficient processing of medical text
   - Reliable API integration
   - Comprehensive logging and monitoring

3. **User Experience**
   - Clear and formatted output
   - Multiple input methods
   - Helpful error messages
   - Intuitive command-line interface

### Feedback and Future Improvements

1. **Current Limitations**
   - Limited to heart failure guidelines
   - Requires internet connection for API
   - Dependent on OpenAI API availability
   - Basic command-line interface

2. **Planned Improvements**
   - **Feature Enhancements**:
     - Web interface development
     - Support for more guideline types
     - Offline recommendation generation
     - Multi-language support

   - **Technical Improvements**:
     - Enhanced error recovery
     - Improved input validation
     - Better performance optimization
     - Extended test coverage

   - **User Experience**:
     - Graphical user interface
     - Mobile application
     - Batch processing improvements
     - Enhanced output formatting

3. **Security Considerations**
   - Implement rate limiting
   - Add user authentication
   - Enhance data privacy
   - Secure API key management

4. **Performance Optimizations**
   - Cache frequently used guidelines
   - Optimize API calls
   - Improve response times
   - Reduce resource usage

