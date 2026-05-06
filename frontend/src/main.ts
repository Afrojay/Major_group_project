import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './styles/main.css'

// Import all components
import {
  Button,
  Card,
  MetricCard,
  SignCard,
  Toast,
  LoadingSpinner,
  Breadcrumb,
  FormGroup,
  Hero,
  Grid,
  ItemGrid,
  FilterPanel,
} from './components/index.js'

const app = createApp({
  template: '<Toast />',
})

// Create and use Pinia store
const pinia = createPinia()
app.use(pinia)

// Register components globally
app.component('Button', Button)
app.component('Card', Card)
app.component('MetricCard', MetricCard)
app.component('SignCard', SignCard)
app.component('Toast', Toast)
app.component('LoadingSpinner', LoadingSpinner)
app.component('Breadcrumb', Breadcrumb)
app.component('FormGroup', FormGroup)
app.component('Hero', Hero)
app.component('Grid', Grid)
app.component('ItemGrid', ItemGrid)
app.component('FilterPanel', FilterPanel)

// Mount the app
app.mount('#app')

export default app

