from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utilities import get_tenant, all_tenants, get_collection_name
from .models import Member
import requests
from django.http import HttpResponse
import base64
import json
from django.http import JsonResponse
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv, dotenv_values
import os

# Create your views here.
def login_view(request):
    ten = all_tenants(request)
    tenant = get_tenant(request)
    if not tenant:
        return render(request, 'registration/login.html', {'error': 'Invalid tenant'})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Get all members of the current tenant
        members = Member.objects.filter(tenant=tenant)
        if any(member.name == username for member in members):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid password', 'tenant': tenant})
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username', 'tenant': tenant})
    else:
        return render(request, 'registration/login.html', {'tenant': tenant, 'all_tenants': ten})



    
@login_required
def main_view(request):
    tenant = get_tenant(request)
    return render(request, 'main.html', {'tenant': tenant})

@login_required
def upload_data(request):
    collection_name = get_collection_name(request)
    return render(request, 'upload_data.html', {'collection_name': collection_name})


# api views

@login_required
def create_collection(request):
    bucket_name = get_collection_name(request)
    collection = get_collection_name(request)

    if request.method == 'POST':
        payload = {
        "bucket_name": bucket_name,
        "collection": collection
        }
        response = requests.post("http://52.21.238.142:80/create_collection", json=payload)

        print(response.text)
        print(response.status_code)
        return redirect('upload_data')
    else:
        return HttpResponse('Invalid request')
    
@login_required
def add_docs(request):
    load_dotenv()
    collection = get_collection_name(request)
    bucket_name = get_collection_name(request)

    bucket_name = bucket_name.replace('_', '-')

    # Read AWS credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
    aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
    region_name = os.getenv('AWS_REGION')

    # Create S3 client with credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError:
        # If bucket does not exist, create it
        s3_client.create_bucket(Bucket=bucket_name)

    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,  # Set to False to disable blocking public ACLs
            'IgnorePublicAcls': False,  # Set to False to ignore public ACLs
            'BlockPublicPolicy': False,  # Set to False to disable blocking public policies
            'RestrictPublicBuckets': False  # Set to False to restrict public buckets
        }
    )


    if request.method == 'POST':
        files = request.FILES.getlist('file')
        
        for file in files:
            try:
                # Upload file to S3 bucket
                s3_client.upload_fileobj(
                    file,
                    bucket_name,
                    file.name
                )
            except ClientError as e:
                print(f"Error uploading {file.name} to S3: {e}")
                return redirect('upload_data')
        
        # Create the payload
        payload = {
            'files': file.name,
            'bucket_name': bucket_name,
            'collection': collection
        }

        response = requests.post(
            "http://52.21.238.142:1024/add_docs",
            json=payload
        )

        if response.status_code == 200:
            return redirect('upload_data')
        else:
            print('error uploading files')
            return redirect('upload_data')
    else:
        return redirect('upload_data')


        
@login_required
def add_doc(request):
    if request.method == 'POST':
        collection = get_collection_name(request)
        text = request.POST.get('uploadtext')

        payload = {
            'text': text,
            'collection': collection
        }

        response = requests.post(
            "http://52.21.238.142:1024/add_doc",
            json=payload
        )

        if response.status_code == 200:
            return redirect('upload_data')
        else:
            print('error uploading text')
            return redirect('upload_data')
        
@login_required
def search_docs(request):
    if request.method == 'GET':
        collection = get_collection_name(request)
        query = request.GET.get('query')
        top_k = request.GET.get('top_k')

        if not query or not top_k:
            return redirect('upload_data')

        try:
            top_k = int(top_k)
        except ValueError:
            return redirect('upload_data')

        payload = {
            'query': query,
            'collection': collection,
            'top_k': top_k
        }

        try:
            response = requests.get(
                "http://52.21.238.142:1024/search_docs",
                json=payload
            )
        except requests.RequestException as e:
            return redirect('upload_data')
        if response.status_code == 200:
            try:
                response_data = response.json()
                ids = response_data.get('ids', [[]])[0]
                context = response_data.get('context', [[]])[0]
                combined_list = [{'id': id_, 'context': ctx} for id_, ctx in zip(ids, context)]

            except ValueError:
                return HttpResponse("Invalid response format from search service.", status=500)
        else:
            return redirect('upload_data')

        return render(request, 'upload_data.html', {'combined_list': combined_list})

    return render(request, 'upload_data.html')



@login_required
def edit_doc(request):
    if request.method == 'POST':
        collection = get_collection_name(request)
        doc_id = request.POST.get('doc_id')
        text = request.POST.get('uploadtext')

        print(doc_id)
        print(text)
        
        payload = {
            'id': doc_id,
            'updated_text': text,
            'collection': collection
        }

        response = requests.post(
            "http://52.21.238.142:1024/edit_doc",
            json=payload
        )

        if response.status_code == 200:
            return redirect('upload_data')
        
        else:
            print('error editing text')
            return redirect('upload_data')
        
    return HttpResponse('Invalid request')


@login_required
def delete_docs(request):
    try:
        collection = get_collection_name(request)
        selected_items_json = request.POST.get('selected_items', '[]')
        selected_items = json.loads(selected_items_json)
        
        print(selected_items)

        # Process each selected item
        for item in selected_items:
            item_id = item['id']

            # Call the external API or perform necessary actions
            payload = {
                'collection': collection,
                'ids': [item_id],
            }
            response = requests.post("http://52.21.238.142:1024/delete_docs", json=payload)
            # Handle the response if needed
            print(response.text)
        return redirect('upload_data')
    except json.JSONDecodeError:
        return redirect('upload_data')
    except Exception as e:
        return redirect('upload_data')


@login_required
def predict(request):
    print('here in predict')
    if request.method == 'POST':
        print('here in predict get')
        collection = get_collection_name(request)
        query = request.POST.get('messageInput')
        top_k = request.POST.get('top_k')

        print(query)
        print(top_k)
        print(collection)

        payload = {
            'query': query,
            'collection': collection,
            'top_k': top_k
        }

        response = requests.post(
            "http://52.21.238.142:1024/predict",
            json=payload
        )
        
        if response.status_code == 200:
            response_data = response.json()
            response = response_data.get('response', {})
            return JsonResponse({'response': response})
        else:
            return HttpResponse("Prediction service returned an error.", status=response.status_code)
        
    return HttpResponse('Invalid request')
