<script setup>

import AdminNavbar from '../../components/AdminNavbar.vue'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'


const token = localStorage.getItem('token')
const router = useRouter()

const companies = ref([])
const search = ref('')


const fetchCompanies = async () => {

  const response = await api.get(
    '/admin/companies',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )


  companies.value = response.data

}



const approveCompany = async (companyId) => {

  await api.put(

      `/admin/company/${companyId}/approve`,

      {},

      {

          headers:{

              Authorization:`Bearer ${token}`

          }

      }

  )

  await fetchCompanies()

}


const viewCompany = (companyId) => {

router.push(
    `/admin/company/${companyId}`
)

}

const showDeactivatedModal = ref(false)

const deactivatedCompanies = ref([])

const fetchDeactivatedCompanies = async () => {

  const response = await api.get(

    "/admin/companies/blacklisted",

    {

      headers: {

        Authorization: `Bearer ${token}`

      }

    }

    )

  deactivatedCompanies.value = response.data

}

const rejectCompany = async (companyId) => {


  const reason = prompt(
    "Enter rejection reason"
  )


  if (!reason) return


  await api.put(

    `/admin/company/${companyId}/reject`,

    {
      reason: reason
    },

    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }

  )
  await fetchCompanies()

  await fetchDeactivatedCompanies()

}


const filteredCompanies = computed(() => {

    return companies.value.filter(company =>

        company.company_name
            .toLowerCase()
            .includes(search.value.toLowerCase())

    )

})

const restoreCompany = async(companyId)=>{

  await api.put(

      `/admin/company/${companyId}/restore`,

      {},

      {

          headers:{

              Authorization:`Bearer ${token}`

          }

      }

  )

  await fetchCompanies()

  await fetchDeactivatedCompanies()

}

const openDeactivatedModal = async () => {

  await fetchDeactivatedCompanies()

  showDeactivatedModal.value = true

}

onMounted(async () => {

  await fetchCompanies()

  await fetchDeactivatedCompanies()

})

</script>



<template>

<AdminNavbar />


<div class="container mt-4">


<h2>
Company Management
</h2>

<button

class="btn btn-outline-danger"

@click="openDeactivatedModal"

>

View Deactivated Companies

</button>



<div class="mb-4">

    <input

        class="form-control"

        v-model="search"

        placeholder="Search company by name"

    >

</div>

<hr>


<h4>
Pending Companies
</h4>


<div
v-for="company in filteredCompanies.filter(c => c.approval_status === 'pending' && !c.is_blacklisted)"
:key="company.id"
class="card p-3 mb-3"
>


<div class="d-flex justify-content-between align-items-start">

    <div>
  
      <h5 class="mb-1">
        {{ company.company_name }}
      </h5>
  
      <p class="mb-1">
        <strong>Industry:</strong>
        {{ company.industry || 'Not Provided' }}
      </p>
  
      <p class="mb-1">
        <strong>Location:</strong>
        {{ company.location || 'Not Provided' }}
      </p>
  
      <p class="mb-0">
        <strong>Website:</strong>
        {{ company.website || 'Not Provided' }}
      </p>
  
    </div>
  
    <span
      class="badge"
      :class="{
        'bg-warning': company.approval_status === 'pending',
        'bg-success': company.approval_status === 'approved',
        'bg-danger': company.approval_status === 'rejected'
      }"
    >
      {{ company.approval_status }}
    </span>
  
  </div>
  
  <hr>


<button
class="btn btn-success me-2"
@click="approveCompany(company.id)"
>

Approve

</button>


<button
class="btn btn-danger"
@click="rejectCompany(company.id)"
>

Reject

</button>


</div>



<hr>


<h4>
Approved Companies
</h4>


<div
v-for="company in filteredCompanies.filter(c => c.approval_status === 'approved' && !c.is_blacklisted)"
:key="company.id"
class="card p-3 mb-3"
>


<h5>
{{ company.company_name }}
</h5>


<button
class="btn btn-primary"
@click="viewCompany(company.id)"
>

View Profile

</button>


</div>


<hr>


<h4>
Rejected Companies
</h4>



<div
v-for="company in filteredCompanies.filter(c => c.approval_status === 'rejected' && !c.is_blacklisted)"
:key="company.id"
class="card p-3 mb-3"
>


<h5>
{{ company.company_name }}
</h5>


<p>

Reason:

{{ company.rejection_reason }}

</p>


</div>



</div>

<div

v-if="showDeactivatedModal"

class="modal d-block"

style="background: rgba(0,0,0,0.5)"

>

<div class="modal-dialog modal-lg">

<div class="modal-content">

<div class="modal-header">

<h5>

Deactivated Companies

</h5>

<button

class="btn-close"

@click="showDeactivatedModal = false"

>

</button>

</div>

<div class="modal-body">

<div

v-if="deactivatedCompanies.length === 0"

class="alert alert-info"

>

No deactivated companies.

</div>

<div

v-for="company in deactivatedCompanies"

:key="company.id"

class="card mb-3"

>

<div class="card-body">

<div class="row">

<div class="col-md-8">

<h5>

{{ company.company_name }}

</h5>

<p>

<strong>Industry:</strong>

{{ company.industry }}

</p>

<p>

<strong>Location:</strong>

{{ company.location }}

</p>

<p>

<strong>Reason:</strong>

{{ company.rejection_reason || 'No reason provided' }}

</p>

</div>

<div class="col-md-4 text-end">

<button

class="btn btn-success"

@click="restoreCompany(company.id)"

>

Restore

</button>

</div>

</div>

</div>

</div>

</div>

<div class="modal-footer">

<button

class="btn btn-secondary"

@click="showDeactivatedModal = false"

>

Close

</button>

</div>

</div>

</div>

</div>
</template>