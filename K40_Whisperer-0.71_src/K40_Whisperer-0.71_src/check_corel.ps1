try {
    $corel = New-Object -ComObject CorelDRAW.Application -ErrorAction Stop
    Write-Host "CorelDRAW detectado..."
    $vbe = $corel.VBE
    # Este é um caminho avançado, pode exigir permissões de 'Confiança no acesso ao modelo de objeto do projeto VBA'
    Write-Host "VBE Object: $vbe"
} catch {
    Write-Host "Não foi possível automatizar o CorelDRAW. Verifique se ele está instalado e se o acesso ao VBA está liberado nas opções de segurança."
}
