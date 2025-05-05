import sys
import os
from dotenv import load_dotenv
import random
load_dotenv()


# Automatically add the project root to sys.path
current_file = os.path.abspath(__file__)
print("Current file :: " , current_file)
project_root = os.path.abspath(os.path.join(current_file, "../../"))  # Adjust depth as needed
if project_root not in sys.path:
    sys.path.insert(0, project_root)


campaign_dir="sales_promotion"

import uuid
import json
import importlib
from sales_promotion.run_dynamic_campaign import load_campaign_plan, dynamic_import_and_execute
from reporting import export_stage_report_by_name

from db import client
from session import session
from datetime import datetime

def load_enterprise_context_sample_by_name(context_name: str) -> dict:
    """
    Loads the given enterprise context from sample_contexts.json by name.
    """
    path = f"campaign/{campaign_dir}/sample_contexts.json"
    try:
        with open(path, "r") as file:
            all_contexts = json.load(file)
            if context_name in all_contexts:
                return all_contexts[context_name]
            else:
                print(f"❌ Context name '{context_name}' not found in sample_contexts.json")
                return {}
    except FileNotFoundError:
        print(f"❌ sample_contexts.json file not found at: {path}")
        return {}



async def insert_campaign_if_not_exists(campaign_id: str):
    """
    Inserts a dummy campaign record if not already present (needed for foreign key).
    """

    existing_campaign = await client.campaign.find_unique(
        where={"id": campaign_id}
    )

    if not existing_campaign:
        await client.campaign.create(
            data={
                "id": campaign_id,
                "name": f"Auto-Created Campaign {campaign_id}",
                "createdAt": datetime.now()
            }
        )
        print(f"✅ Inserted dummy Campaign for ID: {campaign_id}")




async def insert_enterprise_context(context_data: dict, campaign_id: str):
    """
    Inserts EnterpriseContext record into database using Prisma ORM.
    """
    await client.connect()

    # Ensure Campaign exists
    await insert_campaign_if_not_exists(campaign_id)

    await client.enterprisecontext.create(
        data={
            "id": str(uuid.uuid4()),
            "campaignId": campaign_id,
            "companyName": context_data["companyName"],
            "domain": context_data["domain"],
            "businessModel": context_data["businessModel"],
            "background": context_data["background"],
            "currentPain": context_data["currentPain"],
            "goals": context_data.get("goals", ""),
            "createdAt": datetime.now()
        }
    )
    await client.disconnect()





def simulate_campaign(campaign_plan_path: str, campaign_id: str, context_name: str):
    """
    Simulates a full campaign run by setting enterprise context into DB and session.
    """
    campaign_plan = load_campaign_plan(campaign_plan_path)
    context_data = load_enterprise_context_sample_by_name(context_name)


    if not context_data:
        print("\n⚠️ Simulation aborted: Enterprise context not found.\n")
        return

    import asyncio
    asyncio.run(insert_enterprise_context(context_data, campaign_id))

    # Store in session for runtime use
    session["enterprise_context"] = context_data
    print(f"\n🚀 Simulating Campaign: {campaign_id} using context: {context_name}\n")

    for stage in campaign_plan:
        print(f"\n🔷 Stage: {stage['stage']} | 🎯 {stage['goal']}")

        for action in stage["actions"]:
            task = action["task"]
            output = action["output"]
            path = action["path"]

            print(f"➡️  Auto-Running Action: {task} (Output: {output})")
            module_path = path

            function_name = path.split(".")[-1]

            dynamic_import_and_execute(module_path, function_name, campaign_id)

        asyncio.run(export_stage_report_by_name(stage['stage'], campaign_id))

    print("\n🎯🎯🎯 Full Campaign Simulation Completed Successfully!")
    print("\n🔔 Final Session Summary:")
    print(session)


if __name__ == "__main__":

#    campaign_id = str(random.randint(100000, 999999))

    campaign_id = "5"
    
    context_name = "electronics_d2c"
    
    campaign_plan_path = f"campaign/{campaign_dir}/campaign_plan.json"
    
    simulate_campaign(campaign_plan_path, campaign_id, context_name)

