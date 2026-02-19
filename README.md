# RNA Nanoparticle Design Tool (Rnano Designer)

A program for designing siRNA-based lssRNA nanoparticles with basic property screening.

## Project Overview

Rnano Designer is a Python tool for designing RNA nanoparticles that supports multiple geometric shapes (triangle, square, pentagon, hexagon, three-way junction) and automatically generates RNA nanoparticle sequences that meet specific constraint conditions. This tool combines both command-line and web interface modes, making it suitable for researchers to quickly design and screen RNA nanoparticles.

## Features

### Supported Nanoparticle Shapes
- **Triangle**: Basic snowflake-shaped RNA structure
- **Square**: Extended snowflake structure
- **Pentagon**: Pentagon-shaped RNA nanoparticle
- **Hexagon**: Hexagon-shaped RNA nanoparticle
- **3wj (Three Way Junction)**: Three-way junction structure

### Sequence Component Types
- **siRNA (Small Interfering RNA)**: Including Sense siRNA and AntiSense siRNA
- **Hairpin Loop**: Used to form secondary structure
- **Kissing Loop**: Used for intermolecular interactions
- **TetraU (Four U)**: Four uracil linker
- **GC Pairs**: Provide structural stability
- **Overhang**: AA or UU overhang structures

### Energy Constraint Optimization
- **Minimum Free Energy (MFE)**: MFE constraint
- **MFE Frequency**: MFE occurrence frequency constraint
- **MFE Diversity**: MFE diversity constraint
- Uses ViennaRNA package for structure prediction and energy calculation

### Advanced Features
- **Base Substitution**: Configurable base substitution ratio
- **GC Clasp Length**: Configurable GC clasp length
- **Overhang Length**: Configurable overhang length
- **Multiprocessing**: Supports parallel processing for accelerated computation

## Installation Guide

### Requirements
- Python 3.8+
- ViennaRNA package
- PHP 7.4+ (for web interface)
- Bootstrap (frontend framework)

### Installation Steps

1. **Clone the project**
```bash
git clone <repository-url>
cd rnano_re
```

2. **Create virtual environment**
```bash
python -m venv rnano_env
source rnano_env/bin/activate  # Linux/Mac
rnano_env\Scripts\activate    # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt  # If requirements.txt exists
# Or manually install:
pip install viennarna
```

4. **Configure web server** (optional)
- Deploy the project to a PHP-enabled web server
- Ensure PHP and web server are running properly

## Usage

### Command Line Usage

Basic command format:
```bash
python main.py <shape> --sirna-path <path_to_fasta> [options]
```

**Parameter Description:**
- `--sirna-path, -s`: siRNA sequence file path (required)
- `--quantity, -q`: Number of nanoparticles to generate (default: 10)
- `--max-quantity, -m`: Maximum attempts (default: 100)
- `--substitute-ratio, -r`: Base substitution ratio (default: 0)
- `--processes, -p`: Number of parallel processes (default: 8)
- `--output-format, -f`: Output format (json/csv, default: json)
- `--output-filename, -o`: Output filename (default: output)

**Constraint Parameters:**
- `--min-mfe, -minmfe`: Minimum free energy
- `--max-mfe, -maxmfe`: Maximum free energy
- `--min-mfe-frequency, -minfreq`: Minimum MFE frequency
- `--max-mfe-frequency, -maxfreq`: Maximum MFE frequency
- `--min-mfe-diversity, -mindiv`: Minimum MFE diversity
- `--max-mfe-diversity, -maxdiv`: Maximum MFE diversity

**Shape-specific Parameters:**
- `--gc-clasp-length, -g`: GC clasp length
- `--overhang-length, -v`: Overhang length

**Usage Examples:**
```bash
# Generate 10 triangular RNA nanoparticles
python main.py triangle -s sirna.fasta -q 10 -p 4

# Generate hexagonal structures with constraints
python main.py hexagon -s sirna.fasta -q 5 --min-mfe -10 --max-mfe -5

# Use CSV output format
python main.py square -s sirna.fasta -f csv -o my_design
```

### Web Interface Usage

Access `index.html` through a browser for a graphical interface:

1. **Upload siRNA file**: Select a FASTA format siRNA sequence file
2. **Select shape**: Choose nanoparticle shape from dropdown menu
3. **Configure parameters**:
   - Output filename and format
   - Quantity-related parameters
   - Constraint parameters
4. **Shape-specific parameters**: Dynamically display relevant parameters based on selected shape
5. **Submit design**: Click the Submit button to start design

## Input File Formats

### siRNA FASTA File Format
```fasta
>siRNA_1
AAGCUAGCUAGCUAGCUAGC
>siRNA_2
UGCAGCUAGCUAGCUAGCUA
>siRNA_3
GCUAGCUAGCUAGCUAGCUA
```

### Default Sequence File (default.json)
```json
{
    "hairPinLoop": ["UCCG", "GCAA", "UUCG"],
    "kissingLoop": [["AAAGCGGUA", "AAACCGCUA"]]
}
```

## Output Results

Generated results include the following information (JSON format):
```json
{
    "siRNAList": [...],          // Used siRNA sequences
    "hairpinList": [...],        // Used hairpin loop sequences
    "kisspairList": [...],       // Used kissing loop pairs
    "sequence": "...",          // Complete RNA sequence
    "secondStructure": "...",   // Secondary structure prediction
    "minimumFreeEnergy": -15.3,  // Minimum free energy
    "mfeFrequency": 0.85,       // MFE frequency
    "mfeDiversity": 2.1         // MFE diversity
}
```

## Project Architecture

```
rnano_re/
├── main.py                    # Main program entry
├── launch_task.py            # Task execution logic
├── args_parser.py            # Argument parsing
├── index.html                # Web interface
├── submit.php                # PHP form handler
├── check_result.php          # Check result status
├── elements.py               # Element class definitions
├── seq_tools.py              # Sequence utility functions
├── file_tools.py             # File utility functions
├── nanoparticles_pack/      # Nanoparticle structure package
│   ├── snowflake.py         # Snowflake structures (six shapes)
│   ├── others.py            # Other structures (e.g., three-way junction)
│   └── nanoparticles.py     # Base nanoparticle class
└── default_seqs/            # Default sequence files
    └── default.json         # Default hairpin and kissing loop sequences
```

## Workflow

1. **Initialization**: Parse command-line arguments or web form data
2. **Load Sequences**: Read siRNA FASTA file and default sequences
3. **Build Structure**: Construct RNA nanoparticle skeleton based on selected shape
4. **Sequence Assembly**: Assemble siRNA, hairpin loops, and kissing loops into the structure
5. **Structure Optimization**:
   - Perform base substitution (if configured)
   - Use ViennaRNA for structure prediction
   - Check constraint conditions
6. **Result Output**: Save design results to specified format
7. **Task Management**: Organize results by timestamp in `tasks/` directory

## Technical Features

1. **Modular Design**: Various shapes implemented independently, easy to extend
2. **Parallel Computing**: Supports multiprocessing for accelerated design process
3. **Constraint-driven**: Optimize design quality through energy constraints
4. **Dual-mode Support**: Supports both command-line and web interface
5. **Sequence Library Management**: Flexible sequence component management

## Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments

Thanks to the following open-source projects for their support:
- [ViennaRNA](https://www.tbi.univie.ac.at/RNA/) - RNA structure prediction
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- [Python](https://www.python.org/) - Programming language