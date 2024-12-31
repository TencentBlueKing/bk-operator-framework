{{/*
Expand the name of the chart.
*/}}
{{- define "bof_tmp_project.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "bof_tmp_project.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "bof_tmp_project.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "bof_tmp_project.labels" -}}
helm.sh/chart: {{ include "bof_tmp_project.chart" . }}
app.kubernetes.io/name: {{ include "bof_tmp_project.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "bof_tmp_project.selectorLabels" -}}
app.kubernetes.io/name: {{ include "bof_tmp_project.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{/*
controller Selector labels
*/}}
{{- define "bof_tmp_project.controller.selectorLabels" -}}
app.kubernetes.io/name: {{ include "bof_tmp_project.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.role: controller
{{- end }}

{{/*
controller labels
*/}}
{{- define "bof_tmp_project.controller.labels" -}}
helm.sh/chart: {{ include "bof_tmp_project.chart" . }}
app.kubernetes.io/name: {{ include "bof_tmp_project.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.role: controller
{{- end }}


{{/*
Create the name of the service account to use
*/}}
{{- define "bof_tmp_project.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "bof_tmp_project.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}