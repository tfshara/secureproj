# import json
# import boto3
# import traceback
# from main_pipeline import run_pipeline  # you wrap your logic in a function

# codepipeline = boto3.client('codepipeline')

# def lambda_handler(event, context):

#     job_id = event['CodePipeline.job']['id']

#     try:
#         print("Deployment triggered by secure ML pipeline.")

#         decision = run_pipeline()

#         if decision == "DEPLOY":
#             codepipeline.put_job_success_result(jobId=job_id)
#         else:
#             codepipeline.put_job_failure_result(
#                 jobId=job_id,
#                 failureDetails={
#                     'type': 'JobFailed',
#                     'message': 'Risk model blocked deployment'
#                 }
#             )

#     except Exception as e:
#         print(str(e))
#         traceback.print_exc()

#         codepipeline.put_job_failure_result(
#             jobId=job_id,
#             failureDetails={
#                 'type': 'JobFailed',
#                 'message': str(e)
#             }
#         )

#     return "Done"

# def lambda_handler(event, context):
#     return {
#         "version": context.function_version,
#         "status": "Deployment successful"
#     }

from main_pipeline import run_pipeline

def lambda_handler(event, context):
    return run_pipeline()
    