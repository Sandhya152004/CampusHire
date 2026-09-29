<script setup>
import AdminNavbar from '../../components/AdminNavbar.vue'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../api'

const route = useRoute()
const router = useRouter()

const token = localStorage.getItem('token')

const company = ref({})
const drives = ref([])

const fetchCompany = async () => {

  const response = await api.get(
    `/admin/company/${route.params.id}`,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  company.value = response.data
}

const fetchDrives = async () => {

  const response = await api.get(
    `/admin/company/${route.params.id}/drives`,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  drives.value = response.data
}

const deactivateCompany = async () => {

  const reason = prompt(
      "Reason for deactivation"
  )

  if (reason === null) return

  await api.put(

      `/admin/company/${route.params.id}/deactivate`,

      {
          reason: reason
      },

      {
          headers: {
              Authorization: `Bearer ${token}`
          }
      }

  )

  await router.push('/admin/companies')

}

onMounted(() => {
  fetchCompany()
  fetchDrives()
})
</script>

<template>

<AdminNavbar />

<div class="container mt-4">

<button
class="btn btn-outline-secondary mb-3"
@click="router.push('/admin/companies')"
>
← Back to Companies
</button>

<h2>{{ company.company_name }}</h2>

<div class="row mt-4">

<div class="col-md-8">

<div class="card shadow-sm p-4 mb-4">

<h4>Company Information</h4>

<hr>

<p><strong>Industry:</strong> {{ company.industry || 'Not Provided' }}</p>

<p><strong>Location:</strong> {{ company.location || 'Not Provided' }}</p>

<p><strong>Website:</strong> {{ company.website || 'Not Provided' }}</p>

<p><strong>Description:</strong> {{ company.description || 'Not Provided' }}</p>

</div>

<div class="card shadow-sm p-4">

<h4>Placement Drives</h4>

<hr>

<div
v-if="drives.length===0"
class="alert alert-info"
>

No drives created yet.

</div>

<div
v-for="drive in drives"
:key="drive.id"
class="border rounded p-3 mb-3"
>

<h5>{{ drive.job_title }}</h5>

<p>Status:
<strong>{{ drive.status }}</strong>
</p>

<p>
Application Deadline:
{{ drive.application_deadline }}
</p>

</div>

</div>

</div>
<div class="card border-danger shadow-sm mt-4">

<div class="card-body">

<h4 class="text-danger">

Danger Zone

</h4>

<p>

Deactivate this company.

The company will no longer be able to log in.

</p>

<button

class="btn btn-danger"

@click="deactivateCompany"

>

Deactivate Company

</button>

</div>

</div>
<div class="col-md-4">

<div class="card shadow-sm p-4">

<h4>HR Information</h4>

<hr>

<p><strong>Name:</strong> {{ company.hr_name || 'Not Provided' }}</p>

<p><strong>Email:</strong> {{ company.hr_email || 'Not Provided' }}</p>

<p><strong>Phone:</strong> {{ company.hr_contact || 'Not Provided' }}</p>

<hr>

<h5>Status</h5>

<span
class="badge"
:class="{
'bg-success': company.approval_status==='approved',
'bg-warning': company.approval_status==='pending',
'bg-danger': company.approval_status==='rejected'
}"
>

{{ company.approval_status }}

</span>

</div>

</div>

</div>

</div>

</template>