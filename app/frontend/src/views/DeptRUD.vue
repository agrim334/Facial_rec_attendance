<template>
  <div class="home">
    <table>
      <tr v-for='course in courses' :key='course.cid'>
        <courserec :course='course' @updrec='updaterec' @delrec='deleterec'></courserec>
      </tr>
    </table>
    <button id='add' @click='addrec'>Add courses</button>
  </div>

</template>

<script>
// @ is an alias to /src
import courserec from '@/components/RUDCourse.vue';

export default {
  name: 'CourseTable',
  props: {
    courses: Array,
  },
  components: {
    courserec,
  },
  methods: {
    updaterec(coursedat) {
      alert(coursedat);
    },
    deleterec(coursedat) {
      alert(coursedat);
    },
    addrec() {
      alert('sdcf');
    },
  },
};
</script>
