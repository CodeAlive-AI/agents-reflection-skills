namespace SampleTarget;

public class UserService
{
    private readonly int _count = 0;

    public string DisplayName { get; set; } = "User";

    public int CountMethod()
    {
        return _count;
    }
}

public class Program
{
    public static void Main()
    {
        var service = new UserService();
        _ = service.DisplayName;
        var localCount = service.CountMethod();
        Console.WriteLine($"count={localCount}");
    }
}
