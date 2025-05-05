import json
import importlib
from  session import session
import traceback

def load_campaign_plan(filepath: str) -> list:
    """
    Loads the campaign plan from JSON.
    """
    with open(filepath, "r") as file:
        return json.load(file)

def dynamic_import_and_execute(module_path: str, function_name: str, campaign_id: str):
    """
    Dynamically imports the module and executes the function with campaign_id.
    """
    print("Dynmaic invocation :: M=", module_path, "\tF=", function_name, "\tCampaignid=", campaign_id)

    try:
        module = importlib.import_module(module_path)
        func = getattr(module, function_name)
        func(campaign_id)

    except ModuleNotFoundError:
        print(f"❌ Module not found: {module_path}")
        traceback.print_exc()
        
    except AttributeError:
        print(f"❌ Function {function_name} not found in {module_path}")
        traceback.print_exc()

    except Exception as e:
        print(f"❌ Error executing {function_name}: {e}")
        traceback.print_exc()




def run_campaign(campaign_plan_path: str, campaign_id: str):
    """
    Runs the campaign as per the dynamic campaign plan.
    """
    campaign_plan = load_campaign_plan(campaign_plan_path)

    print(f"\n🚀 Starting Campaign Automation for ID: {campaign_id}\n")

    for stage in campaign_plan:
        print(f"\n🔷 Stage: {stage['stage']}\n🎯 Goal: {stage['goal']}\n")

        for action in stage["actions"]:
            task = action["task"]
            output = action["output"]
            path = action["path"]

            print(f"➡️  Running Action: {task} (Output: {output})")
            module_path = path
            function_name = path.split(".")[-1]  # Function name same as file name

            dynamic_import_and_execute(module_path, function_name, campaign_id)

            proceed = input("\n✅ Action completed. Proceed to next action? (yes/no): ").lower()
            if proceed != "yes":
                print("\n🛑 Campaign execution stopped by user.")
                return

    print("\n🎯🎯🎯 Full Campaign Execution Completed Successfully!\n")
    print("🔔 Final Session Summary:")
    print(session)

if __name__ == "__main__":
    campaign_id = input("🔵 Enter new Campaign ID: ").strip()
    campaign_plan_path = "campaign_plan.json"  # Assuming this file is in CWD
    run_campaign(campaign_plan_path, campaign_id)
