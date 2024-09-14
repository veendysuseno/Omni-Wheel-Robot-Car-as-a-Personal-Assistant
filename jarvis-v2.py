import wolframalpha

def vis():
    client = wolframalpha.Client('6ERJK5-T7YX6JGYK7')  # Replace with your WolframAlpha App ID

    print("Welcome to the WolframAlpha CLI. Type 'exit' to quit.")
    while True:
        try:
            query = input('Query: ').strip()
            if query.lower() in ['exit', 'quit', 'q']:  # Allow user to exit
                print("Goodbye!")
                break
            
            res = client.query(query)
            answer = next(res.results).text
            print(f"Answer: {answer}")

        except StopIteration:
            print("Sorry, I couldn't find an answer. Please try asking something else.")

        except Exception as e:
            print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    vis()
