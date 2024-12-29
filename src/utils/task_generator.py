"""
Task generator for hierarchical breakdown of protein engineering tasks.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from pydantic import BaseModel
import yaml

@dataclass
class Task:
    id: str
    name: str
    description: str
    children: List['Task'] = None
    parent_id: Optional[str] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []

class TaskHierarchy:
    def __init__(self, topic: str):
        self.topic = topic
        self.tasks: Dict[str, Task] = {}
        
    def add_task(self, task_id: str, name: str, description: str, parent_id: Optional[str] = None) -> Task:
        task = Task(id=task_id, name=name, description=description, parent_id=parent_id)
        self.tasks[task_id] = task
        
        if parent_id and parent_id in self.tasks:
            parent = self.tasks[parent_id]
            parent.children.append(task)
            
        return task
    
    def to_dict(self) -> dict:
        def task_to_dict(task: Task) -> dict:
            return {
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'children': [task_to_dict(child) for child in task.children] if task.children else []
            }
        
        root_tasks = [task for task in self.tasks.values() if not task.parent_id]
        return {
            'topic': self.topic,
            'tasks': [task_to_dict(task) for task in root_tasks]
        }
    
    def to_yaml(self, file_path: str):
        with open(file_path, 'w') as f:
            yaml.dump(self.to_dict(), f, sort_keys=False, indent=2)

def generate_protein_engineering_tasks() -> TaskHierarchy:
    hierarchy = TaskHierarchy(
        "Engineering plant based protein for sarcopenia reduction"
    )
    
    # 1. Source Selection
    source = hierarchy.add_task(
        "1", "Plant Protein Source Selection",
        "Identify and evaluate optimal plant protein sources"
    )
    
    # 1.1 Source Analysis
    source_analysis = hierarchy.add_task(
        "1.1", "Source Analysis",
        "Comprehensive analysis of potential plant protein sources",
        source.id
    )
    
    hierarchy.add_task(
        "1.1.1", "Amino Acid Profiling",
        "Analyze amino acid compositions of candidate plants",
        source_analysis.id
    )
    
    hierarchy.add_task(
        "1.1.2", "Protein Content Assessment",
        "Measure and compare protein yields",
        source_analysis.id
    )
    
    hierarchy.add_task(
        "1.1.3", "Scalability Evaluation",
        "Assess cultivation and processing scalability",
        source_analysis.id
    )
    
    # 1.2 Quality Metrics
    quality = hierarchy.add_task(
        "1.2", "Quality Assessment",
        "Evaluate protein quality parameters",
        source.id
    )
    
    hierarchy.add_task(
        "1.2.1", "Digestibility Analysis",
        "Measure PDCAAS and digestibility factors",
        quality.id
    )
    
    hierarchy.add_task(
        "1.2.2", "Amino Acid Ratios",
        "Analyze essential amino acid proportions",
        quality.id
    )
    
    # 2. Protein Engineering
    engineering = hierarchy.add_task(
        "2", "Protein Engineering",
        "Modify and optimize protein structure"
    )
    
    # 2.1 Structure Optimization
    structure = hierarchy.add_task(
        "2.1", "Structure Optimization",
        "Enhance protein structure for better absorption",
        engineering.id
    )
    
    hierarchy.add_task(
        "2.1.1", "Folding Enhancement",
        "Optimize protein folding for stability",
        structure.id
    )
    
    hierarchy.add_task(
        "2.1.2", "Bioavailability Modification",
        "Enhance protein bioavailability",
        structure.id
    )

    # 2.2 Absorption Enhancement
    absorption = hierarchy.add_task(
        "2.2", "Absorption Enhancement",
        "Optimize protein absorption mechanisms",
        engineering.id
    )

    hierarchy.add_task(
        "2.2.1", "Enzyme Resistance",
        "Develop protease-resistant structures",
        absorption.id
    )

    hierarchy.add_task(
        "2.2.2", "Transport Enhancement",
        "Improve amino acid transport mechanisms",
        absorption.id
    )
    
    # 3. Clinical Validation
    validation = hierarchy.add_task(
        "3", "Clinical Validation",
        "Validate effectiveness in reducing sarcopenia"
    )
    
    # 3.1 Trial Design
    trials = hierarchy.add_task(
        "3.1", "Trial Design",
        "Design clinical trials for validation",
        validation.id
    )
    
    hierarchy.add_task(
        "3.1.1", "Protocol Development",
        "Develop detailed trial protocols",
        trials.id
    )
    
    hierarchy.add_task(
        "3.1.2", "Outcome Measures",
        "Define and validate outcome measurements",
        trials.id
    )

    # 3.2 Safety Assessment
    safety = hierarchy.add_task(
        "3.2", "Safety Assessment",
        "Comprehensive safety evaluation",
        validation.id
    )

    hierarchy.add_task(
        "3.2.1", "Toxicity Studies",
        "Evaluate potential toxicity risks",
        safety.id
    )

    hierarchy.add_task(
        "3.2.2", "Interaction Analysis",
        "Study drug and nutrient interactions",
        safety.id
    )

    # 4. Manufacturing Process
    manufacturing = hierarchy.add_task(
        "4", "Manufacturing Process",
        "Develop scalable production process"
    )

    # 4.1 Extraction Methods
    extraction = hierarchy.add_task(
        "4.1", "Extraction Methods",
        "Optimize protein extraction process",
        manufacturing.id
    )

    hierarchy.add_task(
        "4.1.1", "Yield Optimization",
        "Maximize protein extraction yield",
        extraction.id
    )

    hierarchy.add_task(
        "4.1.2", "Purity Enhancement",
        "Improve protein purity levels",
        extraction.id
    )

    # 4.2 Scale-up Process
    scaleup = hierarchy.add_task(
        "4.2", "Scale-up Process",
        "Industrial scale production development",
        manufacturing.id
    )

    hierarchy.add_task(
        "4.2.1", "Equipment Specification",
        "Define industrial equipment requirements",
        scaleup.id
    )

    hierarchy.add_task(
        "4.2.2", "Process Validation",
        "Validate production processes",
        scaleup.id
    )

    # 5. Regulatory Compliance
    regulatory = hierarchy.add_task(
        "5", "Regulatory Compliance",
        "Ensure regulatory requirements are met"
    )

    # 5.1 Documentation
    documentation = hierarchy.add_task(
        "5.1", "Documentation",
        "Prepare regulatory documentation",
        regulatory.id
    )

    hierarchy.add_task(
        "5.1.1", "Safety Data",
        "Compile safety documentation",
        documentation.id
    )

    hierarchy.add_task(
        "5.1.2", "Manufacturing Records",
        "Prepare production documentation",
        documentation.id
    )

    # 5.2 Approval Process
    approval = hierarchy.add_task(
        "5.2", "Approval Process",
        "Navigate regulatory approval process",
        regulatory.id
    )

    hierarchy.add_task(
        "5.2.1", "Submission Strategy",
        "Develop regulatory submission plan",
        approval.id
    )

    hierarchy.add_task(
        "5.2.2", "Compliance Monitoring",
        "Monitor ongoing compliance",
        approval.id
    )

    # 6. Market Implementation
    market = hierarchy.add_task(
        "6", "Market Implementation",
        "Plan and execute market launch"
    )

    # 6.1 Distribution
    distribution = hierarchy.add_task(
        "6.1", "Distribution Strategy",
        "Develop distribution network",
        market.id
    )

    hierarchy.add_task(
        "6.1.1", "Channel Development",
        "Establish distribution channels",
        distribution.id
    )

    hierarchy.add_task(
        "6.1.2", "Logistics Planning",
        "Plan product logistics",
        distribution.id
    )

    # 6.2 Market Education
    education = hierarchy.add_task(
        "6.2", "Market Education",
        "Educate stakeholders about product",
        market.id
    )

    hierarchy.add_task(
        "6.2.1", "Healthcare Provider Training",
        "Develop provider education programs",
        education.id
    )

    hierarchy.add_task(
        "6.2.2", "Patient Education",
        "Create patient education materials",
        education.id
    )
    
    return hierarchy

if __name__ == "__main__":
    # Generate task hierarchy
    hierarchy = generate_protein_engineering_tasks()
    
    # Save to YAML
    hierarchy.to_yaml("protein_engineering_tasks.yaml")
