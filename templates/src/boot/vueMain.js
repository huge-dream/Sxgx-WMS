import Print from 'vue-print-nb'
import VDistpicker from 'v-distpicker'
import * as Base64 from 'js-base64'
export default async ({ app, router, store, Vue }) => {
  Vue.component('v-distpicker', VDistpicker)
  Vue.prototype.Base64 = Base64
  Vue.use(Print)
  console.log('Welcome To GreaterWMS')
  console.log('Home Page ------ https://www.56yhz.com/')
  console.log('Demo Page ------ https://production.56yhz.com/')
  console.log('Gitee Page ------ https://gitee.com/Singosgu/GreaterWMS')
  console.log('GitHub Page ------ https://github.com/Singosgu/GreaterWMS')
}
