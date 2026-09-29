<script setup>
import StudentNavbar from '../../components/StudentNavbar.vue'
import { ref, onMounted } from 'vue'
import api from '../../api'

const drives = ref([])
const applications = ref([])

const successMessage = ref('')
const errorMessage = ref('')

const token = localStorage.getItem('token')

const fetchDrives = async () => {

  const response = await api.get(
    '/student/drives',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  drives.value = response.data
}

const fetchApplications = async () => {

  const response = await api.get(
    '/student/applications',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  applications.value = response.data
}

const applyDrive = async (driveId) => {

  try {

    await api.post(
      `/student/apply/${driveId}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    successMessage.value = 'Applied Successfully'
    errorMessage.value = ''

    fetchApplications()

  } catch (error) {

  alert(
    error.response.data.message
  )

  console.log(error)

  }

}

onMounted(() => {

  fetchDrives()
  fetchApplications()

})
</script>

<template>

<StudentNavbar />

<div class="container mt-4">

  <h2 class="mb-4">
    Welcome, Student
  </h2>

  <div
    v-if="successMessage"
    class="alert alert-success"
  >
    {{ successMessage }}
  </div>

  <div
    v-if="errorMessage"
    class="alert alert-danger"
  >
    {{ errorMessage }}
  </div>

  <h4 class="mb-3">
    Available Drives
  </h4>

  <div
    v-if="drives.length === 0"
    class="alert alert-info"
  >
    No placement drives available.
  </div>

  <div
    v-for="drive in drives"
    :key="drive.id"
    class="card shadow-sm mb-3"
  >

    <div class="card-body">

      <h5>{{ drive.job_title }}</h5>

      <p>{{ drive.job_description }}</p>

      <button
        class="btn btn-primary"
        @click="applyDrive(drive.id)"
      >
        Apply
      </button>

    </div>

  </div>

  <hr>

  <h4 class="mb-3">
    My Applications
  </h4>

  <div
    v-if="applications.length === 0"
    class="alert alert-info"
  >
    No applications submitted yet.
  </div>

  <div
    v-for="application in applications"
    :key="application.application_id"
    class="card shadow-sm mb-3"
  >

    <div class="card-body">

      <h5>{{ application.job_title }}</h5>

      <p>
        Status:
        <strong>{{ application.status }}</strong>
      </p>

    </div>

  </div>

</div>

</template>