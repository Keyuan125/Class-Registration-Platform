# Conceptual Design


- Team Name: The-Lab-Rats
- Members:
   - Keyuan Huang (keyuanh2@illinois.edu)
   - Ziyue Guo (ziyueg5@illinois.edu)
   - Yiyan Wang (yiyanw3@illinois.edu)  
- Captain: Keyuan Huang
- Project Title: Course Registration Platform

## ER/UML Diagram

(Insert diagram here)

## Relational Schema

Student (Student_ID INT [PK], Student_Name VARCHAR(100), birth DATE);
Department (Department_ID INT [PK], Department_Name VARCHAR(100));
Account (AID INT [PK], username VARCHAR(100), password VARCHAR(100), Role VARCHAR(100));
Course (CRN INT [PK], Course_Name VARCHAR(100), Professor VARCHAR(100));
Professor (PID INT [PK], Professor_Name VARCHAR(100), info VARCHAR(100));

Belong_to (Department_ID INT [PK] [FK to Department.Department_ID], Student_ID INT [PK] [FK to Student.Student_ID]);
Is (Student_ID INT [PK] [FK to Student.Student_ID], AID INT [PK] [FK to Account.AID]);
Enroll_in (Student_ID INT [PK] [FK to Student.Student_ID], CRN INT [PK] [FK to Course.CRN]);
Offer (Department_ID INT [PK] [FK to Department.Department_ID], CRN INT [PK] [FK to Course.CRN]);
Prereq (CRN INT [PK] [FK to Course.CRN], Pre_CRN INT [PK] [FK to Course.CRN]);
In (PID INT [PK] [FK to Professor.PID], Department_ID INT [PK] [FK to Department.Department_ID]);
Teach (PID INT [PK] [FK to Professor.PID], CRN INT [PK] [FK to Course.CRN]);

## Assumptions and description



