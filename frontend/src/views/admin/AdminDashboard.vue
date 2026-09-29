<script setup>
import AdminNavbar from '../../components/AdminNavbar.vue'
import { ref, onMounted } from 'vue'
import api from '../../api'

const token = localStorage.getItem('token')

const companies = ref([])
const drives = ref([])
const stats = ref({})

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

const fetchDrives = async () => {

  const response = await api.get(
    '/admin/drives',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )


  drives.value = response.data

}

const approveDrive = async (driveId) => {

  try {

    await api.put(
      `/admin/drive/${driveId}/approve`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )


    alert(
      'Drive Approved'
    )


    fetchDrives()


  } catch (error) {

    console.log(error)

  }

}

const rejectDrive = async (driveId) => {


  const reason = prompt(
    'Enter rejection reason'
  )


  if (!reason) return


  try {


    await api.put(
      `/admin/drive/${driveId}/reject`,
      {
        reason: reason
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )


    alert(
      'Drive Rejected'
    )


    fetchDrives()


  } catch (error) {

    console.log(error)

  }


}

const approveCompany = async (companyId) => {

  await api.put(

      `/admin/company/${companyId}/approve`,

      {},

      {
          headers: {
              Authorization: `Bearer ${token}`
          }
      }

  )

  await fetchCompanies()

}

const rejectCompany = async (companyId) => {

const reason = prompt("Enter rejection reason")

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

const fetchStats = async () => {

  const response = await api.get(
    '/admin/stats',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  stats.value = response.data

}

onMounted(() => {

  fetchCompanies()
  fetchDrives()
  fetchStats()

})
</script>

<template>

  <AdminNavbar />

  <div class="container mt-4">

    <h2 class="mb-4">
      Placement Administration
    </h2>

    <div class="row mb-4">

      <div class="col-md-3">
        <div class="card shadow-sm p-3">
          <h6>Students</h6>
          <h2>{{ stats.students }}</h2>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm p-3">
          <h6>Companies</h6>
          <h2>{{ stats.companies }}</h2>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm p-3">
          <h6>Drives</h6>
          <h2>{{ stats.drives }}</h2>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card shadow-sm p-3">
          <h6>Applications</h6>
          <h2>{{ stats.applications }}</h2>
        </div>
      </div>

    </div>

    <hr>

    <h4 class="mb-3">
      Registered Companies
    </h4>

    <div v-if="companies.length === 0" class="alert alert-info">
      No companies found.
    </div>

    <div v-for="company in companies" :key="company.id" class="card shadow-sm p-3 mb-3">

      <h5>{{ company.company_name }}</h5>

      <p>
        Status:
        <strong>{{ company.approval_status }}</strong>
      </p>

      <div v-if="company.approval_status === 'pending'">

        <button class="btn btn-success me-2" @click="approveCompany(company.id)">
          Approve
        </button>

        <button class="btn btn-danger" @click="rejectCompany(company.id)">
          Reject
        </button>

      </div>

      <div v-else-if="company.approval_status === 'approved'">

        <span class="badge bg-success">
          Approved
        </span>

      </div>

      <div v-else-if="company.approval_status === 'rejected'">

        <span class="badge bg-danger">
          Rejected
        </span>

        <p class="mt-2 mb-0">
          <strong>Reason:</strong>
          {{ company.rejection_reason }}
        </p>

      </div>

    </div>
    <hr>


    <h4 class="mb-3">
      Placement Drives
    </h4>


    <div v-if="drives.length === 0" class="alert alert-info">

      No drives found.

    </div>


    <div v-for="drive in drives" :key="drive.id" class="card shadow-sm p-3 mb-3">


      <h5>
        {{ drive.job_title }}
      </h5>


      <p>
        {{ drive.job_description }}
      </p>


      <p>

        Status:

        <strong>
          {{ drive.status }}
        </strong>

      </p>


      <div v-if="drive.status === 'pending'">


        <button class="btn btn-success me-2" @click="approveDrive(drive.id)">

          Approve

        </button>


        <button class="btn btn-danger" @click="rejectDrive(drive.id)">

          Reject

        </button>


      </div>


      <div v-else-if="drive.status === 'approved'">

        <span class="badge bg-success">
          Approved
        </span>

      </div>


      <div v-else-if="drive.status === 'rejected'">

        <span class="badge bg-danger">
          Rejected
        </span>


        <p>
          Reason:
          {{ drive.rejection_reason }}
        </p>


      </div>


    </div>
  </div>

</template>