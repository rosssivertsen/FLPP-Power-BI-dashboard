// ============================================================================
// FLPP Power BI Dashboard - Power Query M Scripts
// Data Import and Transformation
// ============================================================================
// This file contains Power Query M scripts for importing and transforming
// data from FLPP_All_Data_Merged.xlsx
// ============================================================================

// ============================================================================
// HELPER FUNCTION: Get Excel File Path
// ============================================================================
ExcelFilePath = "data/FLPP_All_Data_Merged.xlsx",

// ============================================================================
// TABLE 1: Completed Services
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    CompletedServices_Sheet = Source{[Item="Completed Services",Kind="Sheet"]}[Data],
    // Promote first row as headers
    PromotedHeaders = Table.PromoteHeaders(CompletedServices_Sheet, [PromoteAllScalars=true]),
    // Remove empty columns (Unnamed: 10, 11, 12)
    RemovedEmptyColumns = Table.SelectColumns(
        PromotedHeaders, 
        {"Branch", "Category", "Type", "Name", "Customer Id", "Customer Name", 
         "Tech Name", "Service Date", "Appt Amount", "Invoice Amount"}
    ),
    // Clean and transform data types
    ChangedType = Table.TransformColumnTypes(RemovedEmptyColumns,{
        {"Branch", type text},
        {"Category", type text},
        {"Type", type text},
        {"Name", type text},
        {"Customer Id", Int64.Type},
        {"Customer Name", type text},
        {"Tech Name", type text},
        {"Service Date", type date},
        {"Appt Amount", type text},  // Will convert currency string to number
        {"Invoice Amount", type text}  // Will convert currency string to number
    }),
    // Clean currency strings and convert to numbers
    CleanedApptAmount = Table.TransformColumns(
        ChangedType,
        {{"Appt Amount", each Text.Replace(Text.Replace(_, "$", ""), ",", ""), type number}}
    ),
    CleanedInvoiceAmount = Table.TransformColumns(
        CleanedApptAmount,
        {{"Invoice Amount", each Text.Replace(Text.Replace(_, "$", ""), ",", ""), type number}}
    ),
    // Trim text fields
    TrimmedText = Table.TransformColumns(CleanedInvoiceAmount, {
        {"Customer Name", Text.Trim, type text},
        {"Tech Name", Text.Trim, type text},
        {"Branch", Text.Trim, type text},
        {"Category", Text.Trim, type text}
    }),
    // Remove rows with null Customer Id
    RemovedNulls = Table.SelectRows(TrimmedText, each [Customer Id] <> null)
in
    RemovedNulls

// ============================================================================
// TABLE 2: Sales by Tech
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    SalesByTech_Sheet = Source{[Item="Sales by Tech",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(SalesByTech_Sheet, [PromoteAllScalars=true]),
    // Clean and transform data types
    ChangedType = Table.TransformColumnTypes(PromotedHeaders,{
        {"Customer Service Category Id", Int64.Type},
        {"Primary Sales Rep", Int64.Type},
        {"Customer Id", type text},  // May need to clean
        {"Customer Name", type text},
        {"Sold Date", type date},
        {"Service Status", type text},
        {"Init Price", type text},
        {"Reg Price", type text},
        {"Category", type text},
        {"Contract Value", type text}
    }),
    // Clean currency strings
    CleanedCurrency = Table.TransformColumns(
        Table.TransformColumns(
            Table.TransformColumns(
                ChangedType,
                {{"Init Price", each Text.Replace(Text.Replace(_, "$", ""), ",", ""), type number}}
            ),
            {{"Reg Price", each Text.Replace(Text.Replace(_, "$", ""), ",", ""), type number}}
        ),
        {{"Contract Value", each Text.Replace(Text.Replace(_, "$", ""), ",", ""), type number}}
    ),
    // Clean Customer Id - convert to number if possible
    CleanedCustomerId = Table.TransformColumns(
        CleanedCurrency,
        {{"Customer Id", each try Number.From(Text.Trim(_)) otherwise null, type nullable number}}
    ),
    // Trim text fields
    TrimmedText = Table.TransformColumns(CleanedCustomerId, {
        {"Customer Name", Text.Trim, type text},
        {"Service Status", Text.Trim, type text},
        {"Category", Text.Trim, type text}
    }),
    // Remove null Customer Id rows
    RemovedNulls = Table.SelectRows(TrimmedText, each [Customer Id] <> null)
in
    RemovedNulls

// ============================================================================
// TABLE 3: Lost Sales
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    LostSales_Sheet = Source{[Item="Lost Sales",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(LostSales_Sheet, [PromoteAllScalars=true]),
    // Remove empty columns
    RemovedEmptyColumns = Table.SelectColumns(
        PromotedHeaders,
        {"Sales Rep", "Acct #", "Customer Name", "Sold Date", "Service Category", "Contract Value"}
    ),
    ChangedType = Table.TransformColumnTypes(RemovedEmptyColumns,{
        {"Sales Rep", type text},
        {"Acct #", Int64.Type},
        {"Customer Name", type text},
        {"Sold Date", type date},
        {"Service Category", type text},
        {"Contract Value", Int64.Type}
    }),
    TrimmedText = Table.TransformColumns(ChangedType, {
        {"Sales Rep", Text.Trim, type text},
        {"Customer Name", Text.Trim, type text},
        {"Service Category", Text.Trim, type text}
    })
in
    TrimmedText

// ============================================================================
// TABLE 4: Customer Detail
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    CustomerDetail_Sheet = Source{[Item="Customer Detail",Kind="Sheet"]}[Data],
    // First row contains headers - use it
    FirstRow = Table.First(CustomerDetail_Sheet),
    Headers = Record.FieldValues(FirstRow),
    // Remove first row and promote headers
    RemovedFirstRow = Table.Skip(CustomerDetail_Sheet, 1),
    PromotedHeaders = Table.PromoteHeaders(RemovedFirstRow, [PromoteAllScalars=true]),
    // Select and rename relevant columns
    SelectedColumns = Table.SelectColumns(
        PromotedHeaders,
        {"Customer Id", "Status", "Branch", "Balance", "Overdue Balance", "Auto Pay",
         "Days Late", "Payment Type", "City", "State", "Zip", "Account Type"}
    ),
    ChangedType = Table.TransformColumnTypes(SelectedColumns,{
        {"Customer Id", Int64.Type},
        {"Status", type text},
        {"Branch", type text},
        {"Balance", type number},
        {"Overdue Balance", type number},
        {"Auto Pay", type text},
        {"Days Late", Int64.Type},
        {"Payment Type", type text},
        {"City", type text},
        {"State", type text},
        {"Zip", type text},
        {"Account Type", type text}
    }),
    // Clean Auto Pay field - convert to boolean
    AddedAutoPayFlag = Table.AddColumn(
        ChangedType,
        "Auto Pay Flag",
        each if Text.Upper([Auto Pay]) = "YES" or Text.Upper([Auto Pay]) = "Y" then true else false,
        type logical
    ),
    TrimmedText = Table.TransformColumns(AddedAutoPayFlag, {
        {"Status", Text.Trim, type text},
        {"Branch", Text.Trim, type text},
        {"Auto Pay", Text.Trim, type text},
        {"Payment Type", Text.Trim, type text},
        {"City", Text.Trim, type text},
        {"State", Text.Trim, type text},
        {"Account Type", Text.Trim, type text}
    }),
    RemovedNulls = Table.SelectRows(TrimmedText, each [Customer Id] <> null)
in
    RemovedNulls

// ============================================================================
// TABLE 5: Tech Reviews
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    TechReviews_Sheet = Source{[Item="Tech Reviews",Kind="Sheet"]}[Data],
    // First row contains headers
    RemovedFirstRow = Table.Skip(TechReviews_Sheet, 1),
    PromotedHeaders = Table.PromoteHeaders(RemovedFirstRow, [PromoteAllScalars=true]),
    // Select and rename columns
    SelectedColumns = Table.SelectColumns(
        PromotedHeaders,
        {"Technician", "Average Star Rating", "Total Ratings", "Account Type"}
    ),
    ChangedType = Table.TransformColumnTypes(SelectedColumns,{
        {"Technician", type text},
        {"Average Star Rating", type number},
        {"Total Ratings", Int64.Type},
        {"Account Type", type text}
    }),
    TrimmedText = Table.TransformColumns(ChangedType, {
        {"Technician", Text.Trim, type text},
        {"Account Type", Text.Trim, type text}
    })
in
    TrimmedText

// ============================================================================
// TABLE 6: Customer Reviews
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    CustomerReviews_Sheet = Source{[Item="Customer Reviews",Kind="Sheet"]}[Data],
    RemovedFirstRow = Table.Skip(CustomerReviews_Sheet, 1),
    PromotedHeaders = Table.PromoteHeaders(RemovedFirstRow, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(
        PromotedHeaders,
        {"Overall Star Rating", "Technician Star Rating", "Comments", "Service Date",
         "Review Date", "Technician", "Service Category", "Appointment Type",
         "Customer Id", "Customer", "Account Type"}
    ),
    ChangedType = Table.TransformColumnTypes(SelectedColumns,{
        {"Overall Star Rating", Int64.Type},
        {"Technician Star Rating", Int64.Type},
        {"Comments", type text},
        {"Service Date", type date},
        {"Review Date", type date},
        {"Technician", type text},
        {"Service Category", type text},
        {"Appointment Type", type text},
        {"Customer Id", Int64.Type},
        {"Customer", type text},
        {"Account Type", type text}
    }),
    TrimmedText = Table.TransformColumns(ChangedType, {
        {"Technician", Text.Trim, type text},
        {"Service Category", Text.Trim, type text},
        {"Appointment Type", Text.Trim, type text},
        {"Customer", Text.Trim, type text},
        {"Account Type", Text.Trim, type text}
    }),
    RemovedNulls = Table.SelectRows(TrimmedText, each [Customer Id] <> null)
in
    RemovedNulls

// ============================================================================
// TABLE 7: Top Rep Index
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    TopRepIndex_Sheet = Source{[Item="Top Rep Index",Kind="Sheet"]}[Data],
    RemovedFirstRow = Table.Skip(TopRepIndex_Sheet, 1),
    PromotedHeaders = Table.PromoteHeaders(RemovedFirstRow, [PromoteAllScalars=true]),
    SelectedColumns = Table.SelectColumns(
        PromotedHeaders,
        {"Rank", "Sales Office", "Sales Rep", "Active", "Auto Pay%", "Auto Pay Rank",
         "Avg Contract Val", "Avg Cont Val Rank", "Index", "Scratch", "Avg Initial Amt Price",
         "Avg Regular Amt", "Avg Contract Length"}
    ),
    ChangedType = Table.TransformColumnTypes(SelectedColumns,{
        {"Rank", Int64.Type},
        {"Sales Office", type text},
        {"Sales Rep", type text},
        {"Active", Int64.Type},
        {"Auto Pay%", type number},
        {"Auto Pay Rank", Int64.Type},
        {"Avg Contract Val", type number},
        {"Avg Cont Val Rank", Int64.Type},
        {"Index", type number},
        {"Scratch", Int64.Type},
        {"Avg Initial Amt Price", type number},
        {"Avg Regular Amt", type number},
        {"Avg Contract Length", type number}
    }),
    TrimmedText = Table.TransformColumns(ChangedType, {
        {"Sales Office", Text.Trim, type text},
        {"Sales Rep", Text.Trim, type text}
    })
in
    TrimmedText

// ============================================================================
// TABLE 8: Financials
// ============================================================================
let
    Source = Excel.Workbook(File.Contents(ExcelFilePath), null, true),
    Financials_Sheet = Source{[Item="Financials",Kind="Sheet"]}[Data],
    // Financials table structure needs to be parsed based on actual layout
    // This is a template - adjust based on actual P&L structure
    PromotedHeaders = Table.PromoteHeaders(Financials_Sheet, [PromoteAllScalars=true]),
    // Remove header rows (rows with company name)
    FilteredRows = Table.SelectRows(
        PromotedHeaders,
        each [Profit and Loss by Month] <> null and 
             [Profit and Loss by Month] <> "FL Pest Pros LLC"
    )
    // Note: Further transformation needed based on actual P&L structure
    // This may require custom parsing logic specific to the P&L format
in
    FilteredRows

// ============================================================================
// DATE TABLE (Required for time-based calculations)
// ============================================================================
let
    // Get date range from Completed Services
    CompletedServices = CompletedServices,  // Reference to Completed Services table
    MinDate = List.Min(Table.Column(CompletedServices, "Service Date")),
    MaxDate = List.Max(Table.Column(CompletedServices, "Service Date")),
    // Create date table
    DateList = List.Dates(MinDate, Duration.Days(MaxDate - MinDate) + 365, #duration(1, 0, 0, 0)),
    DateTable = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}),
    ChangedType = Table.TransformColumnTypes(DateTable, {{"Date", type date}}),
    // Add date attributes
    AddedYear = Table.AddColumn(ChangedType, "Year", each Date.Year([Date]), Int64.Type),
    AddedQuarter = Table.AddColumn(AddedYear, "Quarter", each Date.QuarterOfYear([Date]), Int64.Type),
    AddedMonth = Table.AddColumn(AddedQuarter, "Month", each Date.Month([Date]), Int64.Type),
    AddedMonthName = Table.AddColumn(AddedMonth, "Month Name", each Date.MonthName([Date]), type text),
    AddedYearMonth = Table.AddColumn(AddedMonthName, "Year Month", each Date.ToText([Date], "YYYY-MM"), type text),
    AddedDayOfWeek = Table.AddColumn(AddedYearMonth, "Day of Week", each Date.DayOfWeekName([Date]), type text),
    AddedDayOfWeekNumber = Table.AddColumn(AddedDayOfWeek, "Day of Week Number", each Date.DayOfWeek([Date], Day.Monday), Int64.Type)
in
    AddedDayOfWeekNumber


