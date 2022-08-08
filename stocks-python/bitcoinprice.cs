using System.Net.Http;

// HTTP Client
private static HttpClient client = new HttpClient();

public static async Task Run(TimerInfo myTimer, IAsyncCollector<string> outputEventHubMessage, TraceWriter log)
{
    try
    {
        // API
        var url = "https://www.bitstamp.net/api/v2/ticker/btcusd";

        // 1. HTTP Request
        var request = await client.GetAsync(url);

        // 2. HTTP Response
        var response = await request.Content.ReadAsStringAsync();

        // 3. Update Event Hub Parameter
        await outputEventHubMessage.AddAsync(response);

        log.Info("Event sent to Azure Event Hub!");
    }
    catch (Exception ex)
    {
        log.Error("An error occured: ", ex);
    }
}