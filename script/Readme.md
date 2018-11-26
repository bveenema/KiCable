```cpp
DoesNotApplySymbol = "-" // "N/A", " "
StripCount = 1
Headers = ["Header1", "Header2", ...]
Rows = [ [/* Row 1 values */],[/* Row 2 values */], ... ]

//	STEP 1: Create NetList and ComponentList by parsing XML
NetList: 				[
									{
										netName: "Net-(PIN3-Pad1)",
										nodes: 	[
															{ref: "W4", pin: "2"},
															{ref: "PIN3", pin: "1"}
														]
									},
									...
								]

ComponentList:	[
									{
										ref: "HOUSING1",
										nets: [
														"Net-(HOUSING1-Pad3)",
														"Net-(HOUSING1-Pad2)",
														"Net-(HOUSING1-Pad1)"
													],
										isAnchor: true
									},
									...
								]

Paths: [] // Will be added to througout example

/*	STEP 2:
	Find an "Anchor component" ==> HOUSING1
	Component is a housing ==> Create LABEL, HOUSING and POSITION columns, then populate
	Get Nets for each pin and create Paths
		Pin 1: "Net-(HOUSING1-Pad1)" ==> Path0
		Pin 2: "Net-(HOUSING1-Pad2)" ==> Path1
		Pin 3: "Net-(HOUSING1-Pad3)" ==> Path2
	Remove HOUSING1 from Component List
*/
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad1)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad2)"],
						complete: false
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: false
					}
				]

/* STEP 3: Get component and add columns, then fill cells
	Get the next components for each path, add to paths (look in NetList)
		- Path0: "Net-(HOUSING1-Pad1)" ==> PIN2 
				==> Component is pin, add PIN and WIRE - STRIP X columns (X is strip count) - increment Strip Count
				==> populate cells
				==> Remove PIN2 from ComponentList
		- Path1: "Net-(HOUSING1-Pad2)" ==> PIN1 
				==> PIN and WIRE - STRIP X columns exist
				==> populate
				==> Remove PIN1 from ComponentList
		- Path2: "Net-(HOUSING1-Pad3)" ==> All node refs are in path, mark complete, populate empty cells with "DoesNotApplySymbol"
*/
StripCount = 2;
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1", "PIN2"],
						nets: ["Net-(HOUSING1-Pad1)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1"],
						nets: ["Net-(HOUSING1-Pad2)"],
						complete: false
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* STEP 4: Get Next Net
	Get the next nets for each path, add to paths (Look in ComponentList)
		- Path0: "PIN2" ==> "Net-(PIN2-Pad2)"
		- Path1: "PIN1" ==> "Net-(PIN1-Pad2)"
		- Path2: completed, no action
*/
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1", "PIN2"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)"],
						complete: false
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]

/* STEP 5:
	Repeat steps 3 and 4 until all paths are complete
	*** For thought completeness, all iterations listed out here ***
*/
/* Interation 2a
	Get the next components for each path, add to paths (look in NetList)
		- Path0: "Net-(PIN2-Pad2)" ==> W5
				==> Component is wire, add WIRE-COLOR, WIRE-LENGTH, WIRE-SIZE columns
				==> populate cells
				==> Remove W5 from ComponentList
		- Path1: "Net-(PIN1-Pad2)" ==> W4
				==> WIRE-COLOR, WIRE-LENGTH, WIRE-SIZE columns columns exist
				==> populate cells
				==> Remove W4 from ComponentList
		- Path2: complete == true ==> DO NOTHING
*/
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1", "PIN2", "W5"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1", "W4"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)"],
						complete: false
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* Iteration 2b
	Get the next nets for each path, add to paths (Look in ComponentList)
		- Path0: "W5" ==> "Net-(PIN4-Pad1)"
		- Path1: "W4" ==> "Net-(PIN3-Pad1)"
		- Path2: completed, no action
*/
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1", "PIN2", "W5"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)", "Net-(PIN4-Pad1)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1", "W4"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)", "Net-(PIN3-Pad1)"],
						complete: false
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* Interation 3a
	Get the next components for each path, add to paths (look in NetList)
		- Path0: "Net-(PIN4-Pad1)" ==> PIN4
				==> Component is pin, add PIN and WIRE - STRIP X columns (X is strip count) - increment Strip Count
				==> populate cells
				==> Remove PIN4 from ComponentList
		- Path1: "Net-(PIN3-Pad1)" ==> PIN3
				==> PIN and WIRE - STRIP X columns exist
				==> populate cells
				==> Remove PIN3 from ComponentList
		- Path2: complete == true ==> DO NOTHING
*/
StripCount = 3
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1", "PIN2", "W5", "PIN4"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)", "Net-(PIN4-Pad1)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1", "W4", "PIN3"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)", "Net-(PIN3-Pad1)"],
						complete: false
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* Iteration 3b
	Get the next nets for each path, add to paths (Look in ComponentList)
		- Path0: "PIN4" ==> "Net-(HOUSING2-Pad1)"
		- Path1: "PIN3" ==> "Net-(HOUSING2-Pad2)"
		- Path2: completed, no action
*/
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1", "PIN2", "W5", "PIN4"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)", "Net-(PIN4-Pad1)", "Net-(HOUSING2-Pad1)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1", "W4", "PIN3"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)", "Net-(PIN3-Pad1)", "Net-(HOUSING2-Pad2)"],
						complete: false
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* Interation 4a
	Get the next components for each path, add to paths (look in NetList)
		- Path0: "Net-(HOUSING2-Pad1)" ==> HOUSING2
				==> Component is housing, add LABEL, HOUSING and POSITION columns
				==> populate cells
				==> Remove HOUSING2 from ComponentList
		- Path1: "Net-(HOUSING2-Pad2)" ==> HOUSING2
				==> NOT in ComponentList, mark Path1 complete
		- Path2: complete == true ==> DO NOTHING
*/
Paths: 	[
					{
						name: "Path0",
						refs: ["HOUSING1", "PIN2", "W5", "PIN4", "HOUSING2"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)", "Net-(PIN4-Pad1)", "Net-(HOUSING2-Pad1)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1", "W4", "PIN3"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)", "Net-(PIN3-Pad1)", "Net-(HOUSING2-Pad2)"],
						complete: true
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* Iteration 4b
	Get the next nets for each path, add to paths (Look in ComponentList)
		- Path0: "HOUSING2" ==> "Net-(HOUSING2-Pad2)" and "Net-(HOUSING2-Pad3)", split path
				==> Path0.0 = old path - "Net-(HOUSING2-Pad2)"
				==> Path0.1 = branch path - "Net-(HOUSING2-Pad3)" (add HOUSING2 ref and net)
		- Path1: completed, no action
		- Path2: completed, no action
*/
Paths: 	[
					{
						name: "Path0.0",
						refs: ["HOUSING1", "PIN2", "W5", "PIN4", "HOUSING2"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)", "Net-(PIN4-Pad1)", "Net-(HOUSING2-Pad1)", "Net-(HOUSING2-Pad2)"],
						complete: false,
						branches: 1,
					},
					{
						name: "Path0.1",
						refs: ["HOUSING2"],
						nets: ["Net-(HOUSING2-Pad3)"],
						complete: false
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1", "W4", "PIN3"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)", "Net-(PIN3-Pad1)", "Net-(HOUSING2-Pad2)"],
						complete: true
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* Iteration 5a
	Get the next components for each path, add to paths (look in NetList)
		- Path0.0: "Net-(HOUSING2-Pad2)" ==> PIN3
				==> NOT in ComponentList --> Mark Path0.0 Complete
		- Path0.1: "Net-(HOUSING2-Pad3)"
				==> All node refs are in path, mark complete, populate empty cells with "DoesNotApplySymbol"
		- Path1: complete == true ==> DO NOTHING
		- Path2: complete == true ==> DO NOTHING
*/
Paths: 	[
					{
						name: "Path0.0",
						refs: ["HOUSING1", "PIN2", "W5", "PIN4", "HOUSING2"],
						nets: ["Net-(HOUSING1-Pad1)", "Net-(PIN2-Pad2)", "Net-(PIN4-Pad1)", "Net-(HOUSING2-Pad1)", "Net-(HOUSING2-Pad2)"],
						complete: true,
						branches: 1,
					},
					{
						name: "Path0.1",
						refs: ["HOUSING2"],
						nets: ["Net-(HOUSING2-Pad3)"],
						complete: true
					},
					{
						name: "Path1",
						refs: ["HOUSING1", "PIN1", "W4", "PIN3"],
						nets: ["Net-(HOUSING1-Pad2)", "Net-(PIN1-Pad2)", "Net-(PIN3-Pad1)", "Net-(HOUSING2-Pad2)"],
						complete: true
					},
					{
						name: "Path2",
						refs: ["HOUSING1"],
						nets: ["Net-(HOUSING1-Pad3)"],
						complete: true
					}
				]
/* Iteration 5b
	Get the next nets for each path, add to paths (Look in ComponentList)
		- Path0.0: completed, no action
		- Path0.1: completed, no action
		- Path1: completed, no action
		- Path2: completed, no action
		==> All Paths COMPLETE reset Paths, StripCount
		==> Go back to Step 2
*/
StripCount = 1
Paths: []
```