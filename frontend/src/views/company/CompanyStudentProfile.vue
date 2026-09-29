<script setup>

import CompanyNavbar from '../../components/CompanyNavbar.vue'

import { ref, onMounted } from 'vue'

import { useRoute } from 'vue-router'

import api from '../../api'

const route = useRoute()

const token = localStorage.getItem('token')

const student = ref({})

const fetchStudent = async () => {

    const response = await api.get(

        `/company/student/${route.params.id}`,

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    student.value = response.data

}

onMounted(fetchStudent)

</script>

<template>

    <CompanyNavbar />
    
    <div class="container mt-4">
    
        <h2>
    
            Student Profile
    
        </h2>
    
        <div class="card shadow-sm mt-4">
    
            <div class="card-body">
    
                <h4>
    
                    {{ student.full_name }}
    
                </h4>
    
                <hr>
    
                <p><strong>Degree:</strong> {{ student.degree }}</p>
    
                <p><strong>Branch/Specialization:</strong> {{ student.branch }}</p>
    
                <p><strong>CGPA:</strong> {{ student.cgpa }}</p>
    
                <p><strong>Graduation Year:</strong> {{ student.graduation_year }}</p>
    
                <p><strong>Phone:</strong> {{ student.phone_number }}</p>
    
                <p><strong>Skills:</strong> {{ student.skills }}</p>
    
                <a
    
                    v-if="student.resume_path"
    
                    :href="`/uploads/resumes/${student.resume_path}`"
    
                    target="_blank"
    
                    class="btn btn-primary"
    
                >
    
                    View Resume
    
                </a>
    
            </div>
    
        </div>
    
    </div>
    
    </template>