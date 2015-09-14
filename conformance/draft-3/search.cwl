cwlVersion: cwl:draft-3
"@graph":
- id: index
  class: CommandLineTool
  baseCommand: python
  arguments:
    - valueFrom: input.txt
      position: 1
  requirements:
    - class: CreateFileRequirement
      fileDef:
        - filename: input.txt
          fileContent:
            engine: "cwl:JsonPointer"
            script: job/index_file
  inputs:
    - id: file
      type: File
    - id: index.py
      type: File
      default:
        class: File
        path: index.py
      inputBinding:
        position: 0
  outputs:
    - id: result
      type: File
      outputBinding:
        glob: input.txt
        secondaryFiles:
          - ".idx"

- id: search
  class: CommandLineTool
  baseCommand: python
  inputs:
    - id: file
      type: File
      inputBinding:
        position: 1
        secondaryFiles:
          - ".idx"
    - id: search.py
      type: File
      default:
        class: File
        path: search.py
      inputBinding:
        position: 0
    - id: term
      type: string
      inputBinding:
        position: 2
  outputs:
    - id: result
      type: File
      outputBinding:
        glob: result.txt
  stdout: result.txt

- id: main
  class: Workflow
  inputs:
    - id: infile
      type: File
    - id: term
      type: string
  outputs:
    - id: outfile
      type: File
      source: "#main/search/result"

  steps:
    - id: index
      run: "#index"
      inputs:
        - { id: file, source: "#main/infile" }
      outputs:
        - id: result

    - id: search
      run: "#search"
      inputs:
        - { id: file, source: "#main/index/result" }
        - { id: term, source: "#main/term" }
      outputs:
        - id: result