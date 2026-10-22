// Power BI parameter CsvPath must point to transactions.csv or an approved synchronized source.
let
    Source = Csv.Document(File.Contents(CsvPath), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Headers, {{"transaction_id", type text}, {"date", type date}, {"revenue", Currency.Type}, {"cost", Currency.Type}, {"resolved", Int64.Type}, {"resolution_hours", type number}, {"automation_success", Int64.Type}}, "en-US")
in
    Typed
